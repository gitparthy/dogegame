import pygame
import sys
import random
import neat
import os

pygame.init()

WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge & Survive - AI Learning")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

def create_obstacle():
    x = random.randint(30, WIDTH - 30)
    return {"x": x, "y": -20, "speed": random.randint(4, 7), "radius": 18}

def eval_genomes(genomes, config):
    nets = []
    balls = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        balls.append({"x": WIDTH // 2, "y": 540})
        ge.append(genome)

    obstacles = []
    obstacle_timer = 0
    score = 0
    generation = getattr(eval_genomes, 'generation', 0)

    running = True
    while running and len(balls) > 0:
        clock.tick(60)
        score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Spawn obstacles
        obstacle_timer += 1
        if obstacle_timer > 40:
            obstacles.append(create_obstacle())
            obstacle_timer = 0

        for obs in obstacles:
            obs["y"] += obs["speed"]
        obstacles = [o for o in obstacles if o["y"] < HEIGHT + 30]

        # Find nearest obstacle
        nearest = None
        for obs in obstacles:
            if nearest is None or obs["y"] > nearest["y"]:
                nearest = obs

        # Move each AI ball
        to_remove = []
        for i, ball in enumerate(balls):
            if nearest:
                inputs = (
                    ball["x"] / WIDTH,
                    nearest["x"] / WIDTH,
                    nearest["y"] / HEIGHT,
                    (ball["x"] - nearest["x"]) / WIDTH,
                )
            else:
                inputs = (ball["x"] / WIDTH, 0.5, 0, 0)

            output = nets[i].activate(inputs)
            decision = output.index(max(output))

            if decision == 0 and ball["x"] - 20 > 0:
                ball["x"] -= 6
            elif decision == 1 and ball["x"] + 20 < WIDTH:
                ball["x"] += 6

            ge[i].fitness += 0.1

            # Check collision
            for obs in obstacles:
                dist = ((ball["x"] - obs["x"])**2 + (540 - obs["y"])**2) ** 0.5
                if dist < 20 + obs["radius"]:
                    ge[i].fitness -= 5
                    to_remove.append(i)
                    break

        for i in sorted(set(to_remove), reverse=True):
            balls.pop(i)
            nets.pop(i)
            ge.pop(i)

        # Stop after enough time
        if score > 100000:
            break

        # Draw everything
        screen.fill((30, 30, 30))

        for obs in obstacles:
            pygame.draw.circle(screen, (255, 80, 80), (int(obs["x"]), int(obs["y"])), obs["radius"])

        for ball in balls:
            pygame.draw.circle(screen, (0, 200, 255), (int(ball["x"]), 540), 20)

        gen_text = font.render(f"Generation: {generation}", True, (255, 255, 0))
        alive_text = font.render(f"Alive: {len(balls)}", True, (200, 200, 200))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))

        screen.blit(gen_text, (10, 10))
        screen.blit(alive_text, (10, 40))
        screen.blit(score_text, (10, 70))
        pygame.display.flip()

    eval_genomes.generation = generation + 1

def run():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-neat.txt")

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    population.run(eval_genomes, 50)

if __name__ == "__main__":
    run()