# cosmic_ray_parallel

Cosmic Ray execution engine that uses multiple threads for speedup. This is
ideal for running cosmic ray on just one computer with a lot of cpus. The celery
executor requires more setup, and the local executor only uses one thread.

It does use one thread per cpu, and is not configure able.

This is extremely little code


