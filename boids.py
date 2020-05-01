import multiprocessing
import os
import sys
import time
from datetime import datetime

import numpy as np
import pygame
from copy import deepcopy
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class bird:
    position = np.array([0,0])
    velocity = 0.0
    direction = np.array([0,0])
    color = None
    default_color = None
    mouse_controlled = False
    size = 1.0
    def __init__(self, position, center, mouse_controlled=False, size=1.0):
        self.position = position
        self.direction = unit_vector(np.array([center[0]-position[0],center[1]-position[1]]))
        self.color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        self.default_color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        self.mouse_controlled = mouse_controlled
        self.size = size

    def step(self, birds, target):
        flock = []
        r, g, b = self.color[0],self.color[1],self.color[1]
        for tmp_bird in birds:
            if tmp_bird != self and pt_dist(self.position, tmp_bird.position) <= (radius * self.size):
                if int(radius*self.size/10) >= pt_dist(self.position, tmp_bird.position) and eating and self.size > tmp_bird.size:
                    self.size = abs_max_size - (abs_max_size-(tmp_bird.size + self.size) if (tmp_bird.size + self.size) <= abs_max_size else 0)
                    if(tmp_bird.mouse_controlled):
                        limit = False
                    birds.remove(tmp_bird)
                else:
                    r += tmp_bird.color[0]
                    g += tmp_bird.color[1]
                    b += tmp_bird.color[2]
                    flock.append(tmp_bird)
        
        new_dir = np.array([0,0])

        if len(flock) > 0:
            index = 0
            for i in range(len(flock)):
                index = i if flock[i].size > flock[index].size else index
            default_color_ratio = 1
            color_ratio = 1
            flock_leader_ratio = 5
            r = int((self.default_color[0] * default_color_ratio + flock_leader_ratio * len(flock) * flock[index].color[0] + color_ratio * self.color[0])/(len(flock)*flock_leader_ratio + default_color_ratio + color_ratio))
            g = int((self.default_color[1] * default_color_ratio + flock_leader_ratio * len(flock) * flock[index].color[1] + color_ratio * self.color[1])/(len(flock)*flock_leader_ratio + default_color_ratio + color_ratio))
            b = int((self.default_color[2] * default_color_ratio + flock_leader_ratio * len(flock) * flock[index].color[2] + color_ratio * self.color[2])/(len(flock)*flock_leader_ratio + default_color_ratio + color_ratio))
            self.color = (r,g,b)
            sep_vec = separation_vec_calc(flock,self)
            ali_vec = allignment_vec_calc(flock,self)
            coh_vec = cohesion_vec_calc(flock,self)
            #print(sep_vec, ali_vec, coh_vec)
        if not self.mouse_controlled:
            
            if len(flock) > 0:
                if(not np.array_equal(np.add(new_dir, sep_vec * separation_ratio), np.array([0,0]))):
                    new_dir = (np.add(new_dir, sep_vec * separation_ratio))
                if(not np.array_equal(np.add(new_dir, coh_vec * cohesion_ratio), np.array([0,0]))):
                    new_dir = (np.add(new_dir, coh_vec * cohesion_ratio))
                if(not np.array_equal(np.add(new_dir, ali_vec * alignment_ratio), np.array([0,0]))):
                    new_dir = (np.add(new_dir, ali_vec * alignment_ratio))
            else:
                self.color = ((self.default_color[0]+self.color[0])/2,(self.default_color[1]+self.color[1])/2,(self.default_color[2]+self.color[2])/2)

            if(not np.array_equal(np.add(new_dir, np.array([target[0] - self.position[0], target[1] - self.position[1]]) * target_ratio), np.array([0,0]))):
                new_dir = unit_vector(np.add(new_dir, np.array([target[0] - self.position[0], target[1] - self.position[1]]) * target_ratio))
            
            if(np.isnan(angle_between(new_dir, self.direction))):
                self.velocity += pos_acc
                if self.velocity > max_speed * (abs_max_size+1-self.size)/abs_max_size: self.velocity = max_speed * (abs_max_size+1-self.size)/abs_max_size
            elif(int(angle_between(new_dir, self.direction)) % 360 != 0):
                self.velocity = (np.abs(180-(int(angle_between(new_dir, self.direction)) % 360)))/180 * max_speed * (abs_max_size+1-self.size)/abs_max_size
            else:
                self.velocity += pos_acc
                if self.velocity > max_speed * (abs_max_size+1-self.size)/abs_max_size: self.velocity = max_speed * (abs_max_size+1-self.size)/abs_max_size
            if(not np.array_equal(np.add(new_dir, self.direction), np.array([0,0]))):
                new_dir = unit_vector(np.add(new_dir * (new_dir_ratio * (abs_max_size+1-self.size)/abs_max_size), self.direction))
            new_pos = np.add(new_dir * self.velocity/vec_len(new_dir), self.position)
        
            self.direction = new_dir
            self.position = np.array([new_pos[0]%max_x, new_pos[1]%max_y])
        else:
            if len(flock) > 0:
                if(not np.array_equal(np.add(new_dir, sep_vec * separation_controlled_ratio), np.array([0,0]))):
                    new_dir = np.add(new_dir, sep_vec * separation_controlled_ratio)
                if(not np.array_equal(np.add(new_dir, coh_vec * cohesion_controlled_ratio), np.array([0,0]))):
                    new_dir = np.add(new_dir, coh_vec * cohesion_controlled_ratio)
                if(not np.array_equal(np.add(new_dir, ali_vec * alignment_controlled_ratio), np.array([0,0]))):
                    new_dir = np.add(new_dir, ali_vec * alignment_controlled_ratio)
            else:
                self.color = ((self.default_color[0]+self.color[0])/2,(self.default_color[1]+self.color[1])/2,(self.default_color[2]+self.color[2])/2)
                
            if(not np.array_equal(np.add(new_dir, self.direction), np.array([0,0]))):
                new_dir = unit_vector(np.add(np.subtract(pygame.mouse.get_pos(), self.position) * controll_ratio, self.direction)) 
            if(np.isnan(angle_between(new_dir, self.direction))):
                self.velocity = pos_acc
            elif(int(angle_between(new_dir, self.direction)) % 360 != 0):
                self.velocity = max_speed/(np.abs(180-(int(angle_between(new_dir, self.direction)) % 360))) * max_speed * (abs_max_size+1-self.size)/abs_max_size
            else:
                self.velocity += pos_acc
                if self.velocity > max_speed: self.velocity = max_speed * (abs_max_size+1-self.size)/abs_max_size
            new_pos = np.add(new_dir * self.velocity/vec_len(new_dir), self.position)
        
            self.direction = new_dir
            self.position = np.array([new_pos[0]%max_x, new_pos[1]%max_y])
        return self


def step(bird_obj, birds, target):
    return bird_obj.step(birds, target)

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def separation_vec_calc(birds, original_bird):
    vec = np.array([0,0])
    for tmp_bird in birds:
        vec_tmp_bird = np.array([original_bird.position[0] - tmp_bird.position[0], original_bird.position[1] - tmp_bird.position[1]])
        vec_tmp_bird = ((radius - vec_len(vec_tmp_bird)) / radius) * vec_tmp_bird
        vec = np.add(vec, vec_tmp_bird  * tmp_bird.size)
    return vec#unit_vector(np.subtract(vec, original_bird.position))

def allignment_vec_calc(birds, original_bird):
    general_dir = original_bird.direction
    for tmp_bird in birds:
        general_dir = np.add(general_dir, tmp_bird.direction * tmp_bird.size)
    general_dir = general_dir/len(birds)
    return np.subtract(general_dir, original_bird.direction)#general_dir/(len(birds)+1)#unit_vector()

def cohesion_vec_calc(birds, original_bird):
    centroid = np.array([0,0])
    for tmp_bird in birds:
        centroid = np.add(centroid, tmp_bird.position)
    centroid = centroid/(len(birds))
    return np.subtract(centroid, original_bird.position)#centroid#unit_vector()

def pt_dist(p_1, p_2):
    return np.sqrt((p_1[0] - p_2[0])**2 + (p_1[1] - p_2[1])**2)

def vec_len(vec):
    return np.sqrt(vec[0]**2 + vec[1]**2)

pos_acc = 1
max_speed = 10
max_x = 1920
max_y = 1000

eating = False

max_size = 20
min_size = 5

abs_max_size = 50

radius = 50

fps_lock = 1/60

separation_ratio = 1
separation_controlled_ratio = 1
alignment_ratio = 1
alignment_controlled_ratio = 1
cohesion_ratio = 1
cohesion_controlled_ratio = 1

target_ratio = 0
controll_ratio = 1
new_dir_ratio = 0.5
bird_count = 50
center = np.array([max_x/2, max_y/2])
target = None

birds = []

#new_pos[0] > max_x*padding or new_pos[1] > max_y*padding or new_pos[0] < max_x-max_x*padding  or new_pos[1] < max_y-max_y*padding:
for i in range(bird_count):
    birds.append(bird(np.array([np.random.randint(max_x - max_x, max_x), np.random.randint(max_y - max_y, max_y)]), center, size=np.random.randint(min_size, max_size)/10))

pygame.init()
size = 10
font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf",size)#pygame.font.SysFont("comicsansms", 72)
size = width, height = max_x, max_y
dark_grey = (50, 50, 50)
screen = pygame.display.set_mode(size)
#pygame.display.toggle_fullscreen()
#pool = multiprocessing.Pool(4)
limit = False
display_text = True
keyEvt = ""
if __name__ == '__main__': 
    #pool = multiprocessing.Pool(1)
    while 1:
        
        
        start = datetime.now()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_bird = bird(np.array(pygame.mouse.get_pos()), center, size=np.random.randint(min_size, max_size)/10)
                    birds.append(new_bird)
                    keyEvt = "%d birds on screen" % len(birds)
                elif event.button == 2:
                    if not limit:
                        target = bird(np.array(pygame.mouse.get_pos()), center, True)
                        birds.append(target)
                        keyEvt = "%d birds on screen" % len(birds)
                        limit = True
                elif event.button == 3:
                    if len(birds) >= 0:
                        keyEvt = "%d birds on screen" % len(birds)
                        if birds.pop(0).mouse_controlled:
                            limit = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                
                #Controlled Boid Ratios
                if keys[pygame.K_s] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and (keys[pygame.K_LALT] or keys[pygame.K_RALT]):
                    separation_controlled_ratio += 0.1
                    keyEvt = "separation_controlled_ratio is set to %f" % separation_controlled_ratio
                elif keys[pygame.K_s] and (keys[pygame.K_LALT] or keys[pygame.K_RALT]):
                    if separation_controlled_ratio > 0:                    
                        separation_controlled_ratio -= 0.1
                    keyEvt = "separation_controlled_ratio is set to %f" % separation_controlled_ratio

                elif keys[pygame.K_a] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and (keys[pygame.K_LALT] or keys[pygame.K_RALT]):
                    alignment_controlled_ratio += 0.1
                    keyEvt = "alignment_controlled_ratio is set to %f" % alignment_controlled_ratio
                elif keys[pygame.K_a] and (keys[pygame.K_LALT] or keys[pygame.K_RALT]):
                    if alignment_controlled_ratio > 0:  
                        alignment_controlled_ratio -= 0.1
                    keyEvt = "alignment_controlled_ratio is set to %f" % alignment_controlled_ratio

                elif keys[pygame.K_c] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and (keys[pygame.K_LALT] or keys[pygame.K_RALT]):
                    cohesion_controlled_ratio += 0.1
                    keyEvt = "cohesion_controlled_ratio is set to %f" % cohesion_controlled_ratio
                elif keys[pygame.K_c] and (keys[pygame.K_LALT] or keys[pygame.K_RALT]):
                    if cohesion_controlled_ratio > 0:
                        cohesion_controlled_ratio -= 0.1
                    keyEvt = "cohesion_controlled_ratio is set to %f" % cohesion_controlled_ratio

                #Boid Ratios
                elif keys[pygame.K_s] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    separation_ratio += 0.1
                    keyEvt = "separation_ratio is set to %f" % separation_ratio
                elif keys[pygame.K_s]:
                    if separation_ratio > 0:
                        separation_ratio -= 0.1
                    keyEvt = "separation_ratio is set to %f" % separation_ratio

                elif keys[pygame.K_a] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    alignment_ratio += 0.1
                    keyEvt = "alignment_ratio is set to %f" % alignment_ratio
                elif keys[pygame.K_a]:
                    if alignment_ratio > 0:
                        alignment_ratio -= 0.1
                    keyEvt = "alignment_ratio is set to %f" % alignment_ratio

                elif keys[pygame.K_c] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    cohesion_ratio += 0.1
                    keyEvt = "cohesion_ratio is set to %f" % cohesion_ratio
                elif keys[pygame.K_c]:
                    if cohesion_ratio > 0:
                        cohesion_ratio -= 0.1
                    keyEvt = "cohesion_ratio is set to %f" % cohesion_ratio

                elif keys[pygame.K_t] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    target_ratio += 0.1
                    keyEvt = "target_ratio is set to %f" % target_ratio
                elif keys[pygame.K_t]:
                    if target_ratio > 0:
                        target_ratio -= 0.1
                    keyEvt = "target_ratio is set to %f" % target_ratio


                elif keys[pygame.K_r] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    radius += 1
                    keyEvt = "radius is set to %d" % radius
                elif keys[pygame.K_r]:
                    if separation_ratio > 0:
                        radius -= 1
                    keyEvt = "radius is set to %d" % radius
                
                elif keys[pygame.K_n] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    new_dir_ratio += 0.1
                    keyEvt = "new_dir_ratio is set to %f" % new_dir_ratio
                elif keys[pygame.K_n]:
                    if new_dir_ratio > 0:
                        new_dir_ratio -= 0.1
                    keyEvt = "new_dir_ratio is set to %f" % new_dir_ratio

                elif keys[pygame.K_v] and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    max_speed += 1
                    keyEvt = "max_speed is set to %d" % max_speed
                elif keys[pygame.K_v]:
                    if max_speed > 0:
                        max_speed -= 1
                    keyEvt = "max_speed is set to %d" % max_speed

                elif keys[pygame.K_d]:
                    display_text = not display_text

                elif keys[pygame.K_e]:
                    eating = not eating
                    keyEvt = "eating is set to %r" % eating
                
        text_status = font.render(keyEvt, True, (255, 255, 255))
        screen.fill(dark_grey)
        #pygame.draw.circle(screen,(100,20,20), center.astype(int), 10, 1)
        #pool.map(itr_bird.step(birds, center), range(0, len(birds) * offset, offset))
        #cp_birds = deepcopy(b)
        for itr_bird in birds:
            max_size = max(max_size, itr_bird.size)
            pygame.draw.circle(screen, itr_bird.color, itr_bird.position.astype(int), int(radius*itr_bird.size/10))#, (5 if itr_bird.mouse_controlled else 1))
            #pygame.draw.circle(screen,(20,100,20),itr_bird.position.astype(int), int(radius * itr_bird.size), 1)
            pygame.draw.line(screen, (255,20,20), itr_bird.position.astype(int), np.add(itr_bird.position,itr_bird.direction*itr_bird.velocity/vec_len(itr_bird.direction)).astype(int), 1)
            step(itr_bird, birds, pygame.mouse.get_pos())
        #print( target.position if limit else center)
        end = datetime.now()
        elapsed = (end.microsecond - start.microsecond)*(10**-6)

        if elapsed < fps_lock:
            time.sleep(min(fps_lock, fps_lock-elapsed))
        
        end = datetime.now()
        elapsed = (end.microsecond - start.microsecond)*(10**-6)
        text = font.render(("%d FPS" % int(1/elapsed)), True, (0, 128, 0))
        if display_text:
            screen.blit(text,(0, 0))
            screen.blit(text_status,(0, max_y-10))
        pygame.display.flip()
