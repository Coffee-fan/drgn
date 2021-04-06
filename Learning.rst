

Casting things: In case of incorrect casting, drgn complains:

>>> prog['slab_caches']
(struct list_head){
	.next = (struct list_head *)0xffff9efb42fb1768,
	.prev = (struct list_head *)0xffff9efb40042068,
}
>>> container_of(prog["slab_caches"].address_of_(), 'struct seq_operations', "list")
Traceback (most recent call last):
  File "<console>", line 1, in <module>
LookupError: 'struct seq_operations' has no member 'list'

struct seq_operations indeed has no member 'list', it does however have a member 'start' per its
definition <Here https://elixir.bootlin.com/linux/v5.2/source/mm/slab_common.c#L1462>

So, the right statement is:

>>> container_of(prog["slab_caches"].address_of_(), 'struct seq_operations', "start")
*(struct seq_operations *)(slab_caches+0x0 = 0xffffffffacf7afe0) = {
	.start = (void *(*)(struct seq_file *, loff_t *))0xffff9efb42fb1768,
	.stop = (void (*)(struct seq_file *, void *))0xffff9efb40042068,
	.next = (void *(*)(struct seq_file *, void *, loff_t *))0x0,
	.show = (int (*)(struct seq_file *, void *))0x0,
}
