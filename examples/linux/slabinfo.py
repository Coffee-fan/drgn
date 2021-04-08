# Copyright (c) Facebook, Inc. and its affiliates.
# SPDX-License-Identifier: GPL-3.0-or-later

"""Emulates /proc/slabinfo"""

"""

NOTE: STILL WORK IN PROGRESS -- 


The call chain is:

proc_create (via) slabinfo_proc_ops

 slabinfo_open (via) slabinfo_show
  slabinfo_show
    print_slabinfo_header
    cache_show 
      get_slabinfo - 
        for_each_kmem_cache_node

The SLUB data structures can be seen here: https://youtu.be/h0VMLXavx30?t=1540

Notes:
    * If an object is not allocated, then the payload points to the next free object.
    * If the object is free, we can poison the object such that access to free data can be 
      detected.

"""
# -- Utility methods --
from drgn import NULL, Object, cast, container_of, execscript, offsetof, reinterpret, sizeof, Type
from typing import Union
from drgn import FaultError

def list_entry(ptr: Object, type: Union[str, Type], member: str) -> Object:
    return container_of(ptr, type, member)



from drgn.helpers.linux import *

_is_config_slab = 'CONFIG_SLAB' in get_kconfig(prog)

from dataclasses import dataclass

@dataclass
class SlabInfo:
    name: str = None
    size: int = 0

    active_objs : int = 0
    num_objs : int = 0
    active_slabs : int = 0
    num_slabs : int = 0
    shared_avail : int = 0
    limit : int = 0
    batchcount : int = 0
    shared : int = 0
    objects_per_slab : int = 0
    pages_per_slab: int = 0
    cache_order : int = None




"""

static inline struct kmem_cache_node *get_node(struct kmem_cache *s, int node)
{
	return s->node[node];
}

#define for_each_kmem_cache_node(__s, __node, __n) \
	for (__node = 0; __node < nr_node_ids; __node++) \
		 if ((__n = get_node(__s, __node)))

#endif

"""


def for_each_kmem_cache_node(s):
    for n in range(len(s.node)):
        thisNode = s.node[n]
        if thisNode:
            yield s.node[n]
        else:
            print("Nada")
    return

def get_slab_slabinfo(s):
    raise NotImplementedError()
    pass

def node_nr_slabs(node):
    nr_slabs : int = 0
    try:
        nr_slabs = int(node.nr_slabs.value_())
    except:
        pass
    return nr_slabs
        
def get_slub_slabinfo(kmem_cache):
    nr_slabs: int = 0
    nr_objs : int = 0
    nr_free : int = 0

#    i = 0
#    print(repr(kmem_cache.node))
#    for n in kmem_cache.node:
#        print(f"i = {i}")
#        i += 1



    dump_kmcn(kmem_cache.node)
    sinfo = SlabInfo()

    # for_each_kmem_cache_node(s, node, n) {
    for node in for_each_kmem_cache_node(kmem_cache):
        #print(f"Node => {node}")
        pass
        #nr_slabs += node_nr_slabs(node)
        #print(repr(node.nr_slabs))
        #nr_slabs += int(node.nr_slabs.value_())
        # nr_slabs += node_nr_slabs(n)
        # nr_objs += node_nr_objs(n)
        # nr_free += count_partial(n, count_free)
    # }

    sinfo.active_objs = nr_objs - nr_free
    sinfo.num_objs = nr_objs
    sinfo.active_slabs = nr_slabs
    sinfo.num_slabs = nr_slabs
    #sinfo.objects_per_slab = oo_objects(s.oo)
    #sinfo.cache_order = oo_order(s.oo)    


    #print(type(s))
    #print(s.name)
    return sinfo


def dump_kmcn(n):
    i: int = 0
    while i < 64:
        obj = n[i]
        try:
            o_ctr = obj.total_objects.counter
            print(f"{i}: Total objects: {o_ctr}")
        except FaultError:
            print(f"{i} is not mapped")
        i += 1
    
def print_slabinfo_header():
    is_config_slab = 'CONFIG_SLAB' in get_kconfig(prog)

    if is_config_slab:
        print("slabinfo - version: 2.1 (statistics)\n")
    else:
        print("slabinfo - version: 2.1\n")
    print("# name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab>", end="")
    print(" : tunables <limit> <batchcount> <sharedfactor>", end="")
    print(" : slabdata <active_slabs> <num_slabs> <sharedavail>")

    if is_config_slab:
        print(" : globalstat <listallocs> <maxobjs> <grown> <reaped> <error> "
            "<maxfreeable> <nodeallocs> <remotefrees> <alienoverflow>")
        print(" : cpustat <allochit> <allocmiss> <freehit> <freemiss>")
    print("\n")


def cache_show(s):
    
    sinfo = get_slabinfo(s)
    pass

def slab_show(kmem_cache):
    s: SlabInfo = get_slabinfo(kmem_cache)
    name: str = kmem_cache.name.string_().decode()
    size = int(kmem_cache.size)
    print(f"{name:17} {s.active_objs:6d} "
          f"{s.num_objs:6d} {size:6d} "
          f"{s.objects_per_slab:4d} {s.pages_per_slab:4d}", end="")
    print(" : tunables "
           f"{s.limit:4d} {s.batchcount:4d} {s.shared:4d}", end="")
    print(" : slabdata "
           f"{s.active_slabs:6d} {s.num_slabs:6d} {s.shared_avail:6d}", end="")

    print("")
    #cache_show(kmem_cache)

# --------------------------------------------------------------------------
# Starts here
# --------------------------------------------------------------------------
get_slabinfo = get_slab_slabinfo if _is_config_slab else get_slub_slabinfo
print_slabinfo_header()
for kmem_cache in list_for_each_entry('struct kmem_cache',
                    prog['slab_caches'].address_of_(),
                    'list'):
    slab_show(kmem_cache)
    #dump_kmcn(kmem_cache.node)
