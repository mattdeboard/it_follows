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
        else:
            raise NoVictimsException()

    def next_victim(self, victim):
        """Put the current victim back onto the stack, and target `victim`
        instead.
        """
        self.victims.append(self.current_victim)
        self.current_victim = victim


class Victim:
    def __init__(self, starting_location):
        # `starting_location` is a string representing a file system path.
        self.location = starting_location
        self.dead = False

    def move(self):
        """Move to a random location in the file system."""
        self.location = random.choice(valid_destinations(self.location))

    def infect(self, follower):
        new_victim = Victim(self.location)
        follower.next_victim(new_victim)
        return new_victim


def valid_destinations(a_dir):
    dests = ['..']
    return dests + [
        name for name in os.listdir(a_dir)
        if os.path.isdir(os.path.join(a_dir, name))
    ]


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


def random_directory(root):
    return random.choice(os.listdir(root))


if __name__ == '__main__':
    victim = Victim(random_directory('~'))
    follower = Follower(random_directory('~'), victim)

    while not victim.dead:
        time.sleep(random.random())
        victim.move()
        time.sleep(follower.speed)
        follower.move()


