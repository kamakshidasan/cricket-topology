/**
 * Base64Decoder - Adapted by Lee Hollingdale from http://www.webtoolkit.info/
 */
 
var Base64Decoder = 
{ 
	_keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
 
	decode : function (input) 
	{
		var output = "";
		var chr1, chr2, chr3;
		var enc1, enc2, enc3, enc4;
		var i = 0;
 
		input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
 
		while (i < input.length) {
 
			enc1 = this._keyStr.indexOf(input.charAt(i++));
			enc2 = this._keyStr.indexOf(input.charAt(i++));
			enc3 = this._keyStr.indexOf(input.charAt(i++));
			enc4 = this._keyStr.indexOf(input.charAt(i++));
 
			chr1 = (enc1 << 2) | (enc2 >> 4);
			chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
			chr3 = ((enc3 & 3) << 6) | enc4;
 
			output = output + String.fromCharCode(chr1);
 
			if (enc3 !== 64) {
				output = output + String.fromCharCode(chr2);
			}
			if (enc4 !== 64) {
				output = output + String.fromCharCode(chr3);
			}
 
		}
  
		return output;
 	}
}; 

   /**
     * Data type for a cricket ball trajectory. Parsers up-stream handle parsing from the various
     * different source formats.
     */
    CricketBallTrajectory = function() {};

	// Adhitya: Constructor for CricketBallTrajectory

	function BallTrajectory(traj){
		newTraj = new CricketBallTrajectory();
		newTraj.bp = traj.bp;
		newTraj.bt = traj.bt;
		newTraj.a = traj.a;
		newTraj.ebv = traj.ebv;
		newTraj.obv = traj.obv;
		newTraj.oba = traj.oba;
		newTraj.bh = traj.bh;
		newTraj.period = traj.period;
		return newTraj;
	}

    /**
     * Gets the ball position at a particular time.
     */
    CricketBallTrajectory.prototype.getExpectedPositionAtTime = function ( t ) {
        var time = t - this.bt;

        return { x: this.getX( this.bp.x, this.ebv.x, this.a.x, time ),
                 y: this.getYorZ( this.bp.y, this.ebv.y, this.a.y, time ),
                 z: this.getYorZ( this.bh, this.ebv.z, this.a.z, time ) };
    };

    /**
     * Gets the ball position at a particular time.
     */
    CricketBallTrajectory.prototype.getPositionAtTime = function ( t ) {
        var time = t - this.bt;

        if ( time > 0 ) {
            return { x: this.getX( this.bp.x, this.obv.x, this.oba.x, time ),
                     y: this.getYorZ( this.bp.y, this.obv.y, this.oba.y, time ),
                     z: this.getYorZ( this.bh, this.obv.z, this.oba.z, time ) };
        }
        else {
            return { x: this.getX( this.bp.x, this.ebv.x, this.a.x, time ),
                     y: this.getYorZ( this.bp.y, this.ebv.y, this.a.y, time ),
                     z: this.getYorZ( this.bh, this.ebv.z, this.a.z, time ) };
        }
    };

    /**
     * Gets the time at a particular X position.
     */
    CricketBallTrajectory.prototype.getTimeAtX = function ( x ) {
        if ( this.bp.x > x ) {
            return Math.log( ( ( x - this.bp.x ) * ( this.oba.x / this.obv.x ) ) + 1 ) / this.oba.x;
        }
        else {
            return Math.log( ( ( x - this.bp.x ) * ( this.a.x / this.ebv.x ) ) + 1 ) / this.a.x;
        }
    };

    /**
     * Gets the x value at a specific time.
     */
    CricketBallTrajectory.prototype.getX = function ( x, vx, ax, t ) {
        return x - ( vx * ( ( 1 - Math.exp( ax * t ) ) / ax ) );
    };

    /**
     * Gets the y or z values at a specific time.
     */
    CricketBallTrajectory.prototype.getYorZ = function ( pos, velocity, accel, t ) {
        return pos + ( velocity * t ) + ( ( accel * t * t ) / 2 );
    };


	/**
     * Parses the trajectory data given.
     */
    parseTrajectory = function ( encoded ) {
        // Raw string is a Base64 encoded stream
        var decoded = Base64Decoder.decode( encoded );

        if ( decoded.length < 72 ) {
            return undefined;
        }

        // Extract coefficients into a trajectory object
        var traj = new CricketBallTrajectory();
        try {
            traj.bp   = readMulti( decoded, 0, 2 );
            traj.bt   = readMulti( decoded, 8, 1 ).x;
            traj.a    = readMulti( decoded, 12, 3 );
            traj.ebv  = readMulti( decoded, 24, 3 );
            traj.obv  = readMulti( decoded, 36, 3 );
            traj.oba  = readMulti( decoded, 48, 3 );
            traj.bh   = readMulti( decoded, 60, 1 ).x;
            //traj.pred = parseBoolean( decoded.substring( 64, 65 ) );
            //traj.xpos = readMulti( decoded, 65, 1 ).x;
            //traj.end = ?
            //traj.trackApproved = parseInt( decoded.substring( 71, 72 ) ) === 1;
            // TODO
            //traj.trackApproved = true;

            // Calculate the period
            var start = traj.getTimeAtX( 18.5 ) + traj.bt;
            var end = traj.getTimeAtX( 0 ) + traj.bt;
            traj.period = { start: start, end: end };
        }
        catch ( exception ) {
            traj.trackApproved = false;
        }

        return traj;
    };

    /**
     * Utility method to read multiple floats from the given data stream.
     */
    readMulti = function ( data, offset, n ) {
        var ret = {};

        if ( n > 0 ) {
            ret.x = decodeFloat( data.substring( offset, offset + 4 ) );
        }
        if ( n > 1 ) {
            ret.y = decodeFloat( data.substring( offset + 4, offset + 8 ) );
        }
        if ( n > 2 ) {
            ret.z = decodeFloat( data.substring( offset + 8, offset + 12 ) );
        }

        return ret;
    };

    /**
     * Decode an IEE754 float.
     */
    decodeFloat = function ( data ) {
        var sign = ( data.charCodeAt( 0 ) & 0x80 ) >> 7;
        var exponent = ( ( data.charCodeAt( 0 ) & 0x7F ) << 1 ) + ( data.charCodeAt( 1 ) >> 7 );

        var significand = 0.0;
        var bit = 23;
        var component = 1.0;
        var b;
        var mask;

        while ( bit >= 0 ) {
            if ( bit === 23 ) {
                b = ( data.charCodeAt( 1 ) & 0x7F ) | 0x80;
                mask = 0x80;
            }
            else if ( bit === 15 ) {
                b = data.charCodeAt( 2 );
                mask = 0x80;
            }
            else if ( bit === 7 ) {
                b = data.charCodeAt( 3 );
                mask = 0x80;
            }

            if ( ( mask & b ) === mask ) {
                significand += component;
            }

            component /= 2;
            mask = mask >> 1;
            bit--;
        }

        return Math.pow( -1, sign ) *
               Math.pow( 2, exponent - 127 ) *
               significand;
    };

getBallOnScreen = function ( oldTraj, time )
{

	traj = new BallTrajectory(oldTraj);

	// Get ball position in real-world coordinates
	var xyz;
	
	if ( time > traj.period.end )
	{
		xyz = traj.getPositionAtTime( traj.period.end );
	}
	else if ( time < traj.period.start )
	{
		xyz = traj.getPositionAtTime( traj.period.start );
	}
	else
	{
		xyz = traj.getPositionAtTime( time );
	}
	return xyz;
};

// Adhitya's own functions

parseStarting = function (encoded)
{
	trajectory = parseTrajectory(encoded);
	return getBallOnScreen(trajectory, trajectory.period.start);

};

timePeriod = function (encoded)
{
	trajectory = parseTrajectory(encoded);
	return trajectory.period.end - trajectory.period.start;

};

parseFlight = function (encoded)
{
	trajectory = parseTrajectory(encoded);
	return trajectory.bt;

};

// Best function for finding the deviation angles
parseExpected = function (encoded)
{
	trajectory = parseTrajectory(encoded);
	traj = new BallTrajectory(trajectory);
	xyz = traj.getExpectedPositionAtTime( traj.period.end );
	return xyz;

};