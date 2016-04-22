# Audiophile Server
>Web interface to view the analyzed data and view a visualization of the determined sound field

### Endpoints
1. GET / - home - for viewing of the sound analysis and viewing the sound field
2. POST /login - used to authenticate robot, *Note: needs only simple key-based authentication for curent purpose*, perhaps two-factor later if the need for multiple robots arises
	* 2 states:
		* if robot - upload new set of frames corresponding to a coordinate (both insert and update)
		* if nonauthenticated user - redirect to home
    * params:
    	* id - authentication code
3. POST /addFrames
	* 2 states:
		* if robot - upload new set of frames corresponding to a coordinate (both insert and update)
		* if nonauthenticated user - redirect to home
    * params:
    	* x - represent dimension of coordinate
    	* y - represent dimension of coordinate
    	* timeS - time series corresponding to sample at coordinate
    	* freqS - frequency series corresponding to sample at coordinate
