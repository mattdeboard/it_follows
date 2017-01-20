#!/usr/bin/env python
"""Simulation of the plot of the 2014 film, _It Follows_."""
import os
import os.path as op
import random
import time
from pathlib import Path


class NoVictimsException(Exception):
    pass


class Follower:
    def __init__(self, starting_location, current_victim=None, speed=.05):
        # `starting_location` is a string representing a file system path.
        self.location = starting_location
        self.current_victim = current_victim
        self.victims = []

        if self.current_victim is not None:
            self.victims.append(self.current_victim)

        self.speed = speed

    def kill_victim(self):
        self.current_victim.dead = True

        try:
            self.current_victim = self.victims.pop()
        except IndexError:
            raise NoVictimsException()

    def move(self):
        if self.location == self.current_victim.location:
            self.kill_victim()
        elif self.current_victim is not None:
            self.location = route_to_dir(self.location,
                                         self.current_victim.location)
            print('Follower location: {}'.format(self.location))
        else:
            raise NoVictimsException()

    def next_victim(self, victim):
        """Put the current victim back onto the stack, and target `victim`
        instead.
        """
        self.victims.append(self.current_victim)
        self.current_victim = victim


class Victim:
    def __init__(self, starting_location, transmission_chance=.25):
        # `starting_location` is a string representing a file system path.
        self.location = starting_location
        self.dead = False
        self.transmission_chance = transmission_chance

    def move(self):
        """Move to a random location in the file system."""
        self.location = op.abspath(
            op.join('.', random.choice(valid_destinations(self.location)))
        )
        print('Victim location: {}'.format(self.location))

    def transmit(self, follower):
        new_victim = Victim(self.location)
        follower.next_victim(new_victim)
        return new_victim


def random_directory(root):
    return op.join(root, random.choice(subdirs(root)))


def route_to_dir(target, destination):
    """Compute a route on the filesystem starting at `target` and ending
    at `destination`.
    """
    common_parent = op.commonprefix([target, destination])

    if target != common_parent:
        return op.abspath(op.join(target, '..'))
    else:
        dest_path = Path(destination)
        relpath = dest_path.relative_to(target)
        return op.join(common_parent, relpath.parts[0])


def subdirs(root):
    return [
        name for name in os.listdir(root)
        if op.isdir(op.join(root, name))
    ]


def valid_destinations(a_dir):
    dests = ['..']
    return dests + subdirs(a_dir)


if __name__ == '__main__':
    root_dir = op.expanduser('~')
    victim = Victim(random_directory(root_dir))
    follower = Follower(random_directory(root_dir), victim)

    while not victim.dead:
        time.sleep(random.random())
        victim.move()

        if random.random() >= victim.transmission_chance:
            victim.transmit(follower)

        time.sleep(follower.speed)
        follower.move()


