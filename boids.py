import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys, pygame
import time


class bird:
    position = np.array([0,0])
    velocity = 0.0
    direction = np.array([0,0])

    def __init__(self, position, center):
        self.position = position
        self.direction = unit_vector(np.array([center[0]-position[0],center[1]-position[1]]))

    def step(self, birds, center):
        flock = []
        for tmp_bird in birds:
            if tmp_bird != self and pt_dist(self.position, tmp_bird.position) <= radius:
                flock.append(tmp_bird)

        new_dir = np.array([0,0])

        if len(flock) > 0:
            sep_vec = separation_vec_calc(flock,self)
            ali_vec = allignment_vec_calc(flock,self)
            coh_vec = cohesion_vec_calc(flock,self)
            if(not np.array_equal(np.add(new_dir, sep_vec * separation_ration), np.array([0,0]))):
                new_dir = unit_vector(np.add(new_dir, sep_vec * separation_ration))
            if(not np.array_equal(np.add(new_dir, coh_vec * cohesion_ration), np.array([0,0]))):
                new_dir = unit_vector(np.add(new_dir, coh_vec * cohesion_ration))
            if(not np.array_equal(np.add(new_dir, ali_vec * alignment_ration), np.array([0,0]))):
                new_dir = unit_vector(np.add(new_dir, ali_vec * alignment_ration))

        if(not np.array_equal(np.add(new_dir, np.array([center[0] - self.position[0], center[1] - self.position[1]]) * center_ration), np.array([0,0]))):
            new_dir = unit_vector(np.add(new_dir, np.array([center[0] - self.position[0], center[1] - self.position[1]]) * center_ration))
        
        #self.velocity += pos_acc
        #if self.velocity > max_speed: self.velocity = max_speed
        #elif self.velocity < -min_speed: self.velocity = -min_speed
        
        if(not np.array_equal(np.add(new_dir, self.direction), np.array([0,0]))):
            new_dir = unit_vector(np.add(new_dir, self.direction))
        if(np.isnan(angle_between(new_dir, self.direction))):
            print(new_dir,self.direction)
            self.velocity = pos_acc
        elif(int(angle_between(new_dir, self.direction)) % 360 != 0):
            self.velocity = max_speed/(int(angle_between(new_dir, self.direction)) % 360)
        else:
            self.velocity += pos_acc
        new_pos = np.add(new_dir * self.velocity/vec_len(new_dir), self.position)
    
        self.direction = new_dir
        self.position = np.array([new_pos[0]%max_x, new_pos[1]%max_y])

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def separation_vec_calc(birds, original_bird):
    vec = np.array([0,0])
    for tmp_bird in birds:
        vec_tmp_bird = np.array([original_bird.position[0]- tmp_bird.position[0], original_bird.position[1]- tmp_bird.position[1]])
        vec = np.add(vec, vec_tmp_bird)
    return unit_vector(np.subtract(vec, original_bird.position))

def allignment_vec_calc(birds, original_bird):
    general_dir = original_bird.direction
    for tmp_bird in birds:
        general_dir = np.add(general_dir, tmp_bird.position)
    return unit_vector(np.subtract(general_dir/(len(birds)+1), original_bird.direction))

def cohesion_vec_calc(birds, original_bird):
    centroid = np.array([0,0])
    for tmp_bird in birds:
        centroid = np.add(centroid, tmp_bird.position)
    centroid = centroid/(len(birds)+1)
    return unit_vector(np.subtract(centroid, original_bird.position))

def pt_dist(p_1, p_2):
    return np.sqrt((p_1[0] - p_2[0])**2 + (p_1[1] - p_2[1])**2)

def vec_len(vec):
    return np.sqrt(vec[0]**2 + vec[1]**2)

pos_acc = 1
neg_acc = 1
max_speed = 20
min_speed = -5
max_x = 160
max_y = 90
padding = 0.9
radius = 50
separation_ration = 1
alignment_ration = 1
cohesion_ration = 1
center_ration = 0
bird_count = 50
center = np.array([max_x/2, max_y/2])
birds = []

#new_pos[0] > max_x*padding or new_pos[1] > max_y*padding or new_pos[0] < max_x-max_x*padding  or new_pos[1] < max_y-max_y*padding:
for i in range(bird_count):
    birds.append(bird(np.array([np.random.randint(max_x-max_x*padding,max_x*padding),np.random.randint(max_y-max_y*padding,max_y*padding)]), center))

pygame.init()

size = width, height = max_x, max_y
dark_grey = (50, 50, 50)

screen = pygame.display.set_mode(size)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    screen.fill(dark_grey)
    #pygame.draw.circle(screen,(100,20,20), center.astype(int), 10, 1)
    for bird in birds:
        pygame.draw.circle(screen,(200,200,200),bird.position.astype(int), 7, 1)
        #pygame.draw.circle(screen,(20,100,20),bird.position.astype(int), radius, 1)
        #pygame.draw.line(screen,(255,20,20),bird.position, np.add(bird.position,bird.direction*bird.velocity/vec_len(bird.direction)), 1)
        bird.step(birds, center)
    pygame.display.flip()
    time.sleep(0.02)
    