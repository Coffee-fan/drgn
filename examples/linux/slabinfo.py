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
def list_entry(ptr: Object, type: Union[str, Type], member: str) -> Object:
    return container_of(ptr, type, member)



from drgn.helpers.linux import *

_is_config_slab = 'CONFIG_SLAB' in get_kconfig(prog)

from dataclasses import dataclass
from ctypes import *

@dataclass
class SlabInfo:
    active_objs : c_ulong = None
    num_objs : c_ulong = None
    active_slabs : c_ulong = None
    num_slabs : c_ulong = None
    shared_avail : c_ulong = None
    limit : c_uint = None
    batchcount : c_uint = None
    shared : c_uint = None
    objects_per_slab : c_uint = None
    cache_order : c_uint = None

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


def for_each_kmem_cache_node(s, n):
    n = 0
    for n in range(0, len(s.node)):
        thisNode = s.node[n]
        if thisNode:
            yield s.node[n]
    return

def get_slab_slabinfo(s):
    raise NotImplementedError()
    pass

def get_slub_slabinfo(s):
    nr_slabs: c_ulong = 0
    nr_objs : c_ulong = 0
    nr_free : c_ulong = 0

    node : int
    n = None

    # for_each_kmem_cache_node(s, node, n) {
    for node in for_each_kmem_cache_node(s, n):
        print(f"Node => {node}")
        # nr_slabs += node_nr_slabs(n)
        # nr_objs += node_nr_objs(n)
        # nr_free += count_partial(n, count_free)
    # }

    sinfo = SlabInfo()
    sinfo.active_objs = nr_objs - nr_free
    sinfo.num_objs = nr_objs
    sinfo.active_slabs = nr_slabs
    sinfo.num_slabs = nr_slabs
    #sinfo.objects_per_slab = oo_objects(s.oo)
    #sinfo.cache_order = oo_order(s.oo)    


    print(type(s))
    print(s.name)
    pass


def print_slabinfo_header():
    is_config_slab = 'CONFIG_SLAB' in get_kconfig(prog)

    if is_config_slab:
        print("slabinfo - version: 2.1 (statistics)\n")
    else:
        print("slabinfo - version: 2.1\n")
    print("# name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab>")
    print(" : tunables <limit> <batchcount> <sharedfactor>")
    print(" : slabdata <active_slabs> <num_slabs> <sharedavail>")

    if is_config_slab:
        print(" : globalstat <listallocs> <maxobjs> <grown> <reaped> <error> "
            "<maxfreeable> <nodeallocs> <remotefrees> <alienoverflow>")
        print(" : cpustat <allochit> <allocmiss> <freehit> <freemiss>")
    print("\n")


def cache_show(s):
    
    sinfo = get_slabinfo(s)
    pass

def slab_show(p):
    # if p.value_() == slab_caches.next.value_():
    #     print("They are equal")

    s = list_entry(p, 'struct kmem_cache', "list")
    print(f"s ==> {s.node}")
    if p == slab_caches.next:
        print_slabinfo_header()
    cache_show(s)

    
# --------------------------------------------------------------------------
# Starts here
# --------------------------------------------------------------------------
print("=" * 80)
get_slabinfo = get_slab_slabinfo if _is_config_slab else get_slub_slabinfo
slab_caches_list = prog['slab_caches']


for kmem_cache in list_for_each_entry('struct kmem_cache', slab_caches_list.address_of_(), 'list'):
    print(kmem_cache.name.string_().decode())
    #print(s)
#    print_node()

#slab_show(slab_caches.next)
#print_slabinfo_header()
#print(slab_caches)
