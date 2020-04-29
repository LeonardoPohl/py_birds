import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys, pygame
import time
import multiprocessing

class bird:
    position = np.array([0,0])
    velocity = 0.0
    direction = np.array([0,0])
    color = None
    default_color = None
    mouse_controlled = False
    def __init__(self, position, center, mouse_controlled=False):
        self.position = position
        self.direction = unit_vector(np.array([center[0]-position[0],center[1]-position[1]]))
        self.color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        self.default_color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        self.mouse_controlled = mouse_controlled

    def step(self, birds, center):
        flock = []
        r, g, b = self.color[0],self.color[1],self.color[1]
        for tmp_bird in birds:
            if tmp_bird != self and pt_dist(self.position, tmp_bird.position) <= radius:
                r += tmp_bird.color[0]
                g += tmp_bird.color[1]
                b += tmp_bird.color[2]
                flock.append(tmp_bird)
        
        new_dir = np.array([0,0])

        if len(flock) > 0:
            index = np.random.randint(0,len(flock))
            r = (self.default_color[0] + len(flock) * flock[index].color[0] + 1*self.color[0])/(len(flock)+2)
            g = (self.default_color[1] + len(flock) * flock[index].color[1] + 1*self.color[1])/(len(flock)+2)
            b = (self.default_color[2] + len(flock) * flock[index].color[2] + 1*self.color[2])/(len(flock)+2)
            self.color = (r,g,b)
            sep_vec = separation_vec_calc(flock,self)
            ali_vec = allignment_vec_calc(flock,self)
            coh_vec = cohesion_vec_calc(flock,self)
        if not self.mouse_controlled:
            
            if len(flock) > 0:
                if(not np.array_equal(np.add(new_dir, sep_vec * separation_ration), np.array([0,0]))):
                    new_dir = unit_vector(np.add(new_dir, sep_vec * separation_ration))
                if(not np.array_equal(np.add(new_dir, coh_vec * cohesion_ration), np.array([0,0]))):
                    new_dir = unit_vector(np.add(new_dir, coh_vec * cohesion_ration))
                if(not np.array_equal(np.add(new_dir, ali_vec * alignment_ration), np.array([0,0]))):
                    new_dir = unit_vector(np.add(new_dir, ali_vec * alignment_ration))
            else:
                self.color = ((self.default_color[0]+self.color[0])/2,(self.default_color[1]+self.color[1])/2,(self.default_color[2]+self.color[2])/2)

            if(not np.array_equal(np.add(new_dir, np.array([center[0] - self.position[0], center[1] - self.position[1]]) * center_ration), np.array([0,0]))):
                new_dir = unit_vector(np.add(new_dir, np.array([center[0] - self.position[0], center[1] - self.position[1]]) * center_ration))
            
            #self.velocity += pos_acc
            #if self.velocity > max_speed: self.velocity = max_speed
            #elif self.velocity < -min_speed: self.velocity = -min_speed
            
            if(not np.array_equal(np.add(new_dir, self.direction), np.array([0,0]))):
                new_dir = unit_vector(np.add(new_dir*new_dir_ratio, self.direction))
            if(np.isnan(angle_between(new_dir, self.direction))):
                #print(new_dir,self.direction)
                self.velocity = pos_acc
            elif(int(angle_between(new_dir, self.direction)) % 360 != 0):
                self.velocity = max_speed/(np.abs(180-(int(angle_between(new_dir, self.direction)) % 360)))
            else:
                #print((new_dir, self.direction))
                #print(int(angle_between(new_dir, self.direction)))
                self.velocity += pos_acc
                if self.velocity>max_speed: self.velocity=max_speed
            new_pos = np.add(new_dir * self.velocity/vec_len(new_dir), self.position)
        
            self.direction = new_dir
            self.position = np.array([new_pos[0]%max_x, new_pos[1]%max_y])
        else:
            if len(flock) > 0:
                if(not np.array_equal(np.add(new_dir, sep_vec * separation_controlled_ration), np.array([0,0]))):
                    new_dir = unit_vector(np.add(new_dir, sep_vec * separation_controlled_ration))
                if(not np.array_equal(np.add(new_dir, coh_vec * cohesion_controlled_ration), np.array([0,0]))):
                    new_dir = unit_vector(np.add(new_dir, coh_vec * cohesion_controlled_ration))
                if(not np.array_equal(np.add(new_dir, ali_vec * alignment_controlled_ration), np.array([0,0]))):
                    new_dir = unit_vector(np.add(new_dir, ali_vec * alignment_controlled_ration))
            else:
                self.color = ((self.default_color[0]+self.color[0])/2,(self.default_color[1]+self.color[1])/2,(self.default_color[2]+self.color[2])/2)

            if(not np.array_equal(np.add(new_dir, np.array([center[0] - self.position[0], center[1] - self.position[1]]) * center_ration), np.array([0,0]))):
                new_dir = unit_vector(np.add(new_dir, np.array([center[0] - self.position[0], center[1] - self.position[1]]) * center_ration))
                
            if(not np.array_equal(np.add(new_dir, self.direction), np.array([0,0]))):
                new_dir = unit_vector(np.add(np.subtract(pygame.mouse.get_pos(), self.position) * controll_ratio, self.direction)) 
            if(np.isnan(angle_between(new_dir, self.direction))):
                #print(new_dir,self.direction)
                self.velocity = pos_acc
            elif(int(angle_between(new_dir, self.direction)) % 360 != 0):
                self.velocity = max_speed/(np.abs(180-(int(angle_between(new_dir, self.direction)) % 360)))
            else:
                #print((new_dir, self.direction))
                #print(int(angle_between(new_dir, self.direction)))
                self.velocity += pos_acc
                if self.velocity>max_speed: self.velocity=max_speed
            new_pos = np.add(new_dir * self.velocity/vec_len(new_dir), self.position)
        
            self.direction = new_dir
            self.position = np.array([new_pos[0]%max_x, new_pos[1]%max_y])
        return self


def step(bird_obj, birds):
    return bird_obj.step(birds, center)

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
max_speed = 10
min_speed = -5
max_x = 1600
max_y = 900
padding = 0.9
radius = 100
separation_ration = 1
separation_controlled_ration = 5
alignment_ration = 1
alignment_controlled_ration = 1
cohesion_ration = 1
cohesion_controlled_ration = 1
center_ration = 0
controll_ratio = 3
new_dir_ratio = 0.5
bird_count = 20
center = np.array([max_x/2, max_y/2])
birds = []

#new_pos[0] > max_x*padding or new_pos[1] > max_y*padding or new_pos[0] < max_x-max_x*padding  or new_pos[1] < max_y-max_y*padding:
for i in range(bird_count):
    birds.append(bird(np.array([np.random.randint(max_x-max_x*padding,max_x*padding),np.random.randint(max_y-max_y*padding,max_y*padding)]), center))

pygame.init()

size = width, height = max_x, max_y
dark_grey = (50, 50, 50)
screen = pygame.display.set_mode(size)
#pygame.display.toggle_fullscreen()
#pool = multiprocessing.Pool(4)
limit = False
if __name__ == '__main__': 
    #pool = multiprocessing.Pool(1)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_bird = bird(np.array(pygame.mouse.get_pos()), center)
                    birds.append(new_bird)
                elif event.button == 2:
                    if not limit:
                        new_bird = bird(np.array(pygame.mouse.get_pos()), center, True)
                        birds.append(new_bird)
                        limit = True
                elif event.button == 3:
                    if birds.pop(0).mouse_controlled:
                        limit = False
        
        screen.fill(dark_grey)
        #pygame.draw.circle(screen,(100,20,20), center.astype(int), 10, 1)
        #*pool.map(itr_bird.step(birds, center), range(0, len(birds) * offset, offset))
        for itr_bird in birds:
            pygame.draw.circle(screen, itr_bird.color,itr_bird.position.astype(int), int(radius/10), 5 if itr_bird.mouse_controlled else 1)
            #pygame.draw.circle(screen,(20,100,20),itr_bird.position.astype(int), radius, 1)
            pygame.draw.line(screen, (255,20,20), itr_bird.position.astype(int), np.add(itr_bird.position,itr_bird.direction*itr_bird.velocity/vec_len(itr_bird.direction)).astype(int), 1)
            step(itr_bird, birds)
        
        
        

        #birds = pool.map(step(itr_bird, birds), [itr_bird for itr_bird in birds])
        #pool.apply(itr_bird.step(birds, center))

        #pool.close()

        pygame.display.flip()
        time.sleep(0.02)
        