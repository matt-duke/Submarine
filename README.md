# Underwater ROV

## Motivation
The inspiration for this project was born on a sunny summer day on Skeleton Lake in Ontario, Canada. This lake is thought to be formed by a meteorite impact about 800 million years ago, followed by several periods of glaciation. This origin story, combined with the lake's crystal clear spring fed water, has resulted in clearly visible incredible underwater topography. However, only a very small portion can be seen from the waters surface, leaving acres of interesting glacial aftermath, submarine rock cliffs and (possibly) optimistic plant life hidden from view and left to the imagination.

<figure>
<p align=center><img src="docs/img/Odale-skeleton-05_skeleton_sw.jpg" width="450"></p>
<figcaption><p align=center>Aerial view of the west side of Skeleton Lake</p></figcaption>
</figure>

The intent of this project has been part practical outcome and part learning experience. So far, the learning portion has been extremely valuable, with many iterations, over-complications and replacements. However, a working prototype is planned for the spring of 2021.

## System Overview
The ROV consists of 3 sperate processors with specific functions dedicated to each. The main processor card (MPC) inside the submarine handles high level monitoring and control tasks, including a database server. It is connected by a CAT5 link to the auxillary processor card (APC), which is on the water's surface and acts as the human to machine interface. This device is intended to receive user commands and send them to the MPC, while displaying critical information with minimal delay.
<figure>
<p align=center><img src="docs/img/system_level.PNG" width="500"></p>
<figcaption><p align=center>System level block diagram</p></figcaption>
</figure>
Because low latency is critical in this application, inter-process communication is accomplished using a Redis server. It acts as an in memory variable cache, with the added ability to act as a message broker. The main redis server lives on the MPC inside the submarine, with a synchronized redis server on the APC acting as a forwarder.

### Hardware


