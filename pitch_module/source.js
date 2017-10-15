var PitchDetection = (function(){
  console.log('Pitch detector loaded')
  var API = {}
  API.mathUtil = (function(){
    var mAPI = {}
    mAPI.detrender = function(array, window){
      var detrended_data = array.slice()
      var pointBasin = window/2
      var dataSize = array.length
      var start = 0
      while(start + window < dataSize){
        var leftBasin = array.slice(start, start+pointBasin);
        var rightBasin = array.slice(start+pointBasin, start+window);
        var leftAverage = leftBasin.reduce((a,b)=>{return a+b})/pointBasin
        var rightAverage = rightBasin.reduce((a,b)=>{return a+b})/pointBasin
        var slope = (rightAverage-leftAverage)/pointBasin
        var b = leftAverage - slope*(start+pointBasin/2)
        for(var index = start; index<start+pointBasin; index++){
          detrended_data[index]-=(slope*index+b)
        }
        start+= pointBasin;
      }
      return detrended_data;
    };
    mAPI.extremaFinder = function(array){
      var prevDelta = 0
      var extrema = []
      for(var index = 0; index<array.length-1; index ++){
        var delta = array[index+1]-array[index]
        if(delta*prevDelta < 0){
          extrema.push(index)
        }
        prevDelta = delta
      }
      return extrema
    }

    mAPI.autoCorrelation = function(array, maxShift){
      var correlates = []
      var size = array.length
      for(var shift= 0; shift < maxShift; shift++){
        var correlation = array.reduce(
          function(total, val, ind, arr){
            return total + arr[ind]*arr[(ind+shift)%size]
          },0)
        correlates.push(correlation)
      }
      return correlates
    }

    mAPI.quadFit = function(x2, yvals){
      // returns a,b,c for ax**2+bx+c assuming y_vals come from points adjacent to x2
      var a = (yvals[0] / 2.0) - yvals[1] + (yvals[2] / 2.0)
      var b = x2*(
              2*yvals[1]-yvals[0]-yvals[2]
          ) - (
              yvals[0]-yvals[2]
          )*0.5
      var c = x2*x2*(
              yvals[0]*0.5- yvals[1]+yvals[2]*0.5
          )+ x2*0.5*(
              yvals[0]-yvals[2]
          )+yvals[1]
      return [a, b, c]
    }

    mAPI.averageGap = function(array){
      var total = array[0]
      for(var ind=1; ind<array.length; ind++){
        total += (array[ind]-array[ind-1])
      }
      return total/(array.length)
    }
    return mAPI
  })()
  API.initialize = function(powers){
    if(typeof(powers)==='undefined'){powers=11}
  }
  return API
})()
/*
from quad_fit_correlation
sub_bin_res takes frequency data, a result from the audio api's fft module
and
  detrends it with window size 80
  autocorrelates out to bin 80 or 21.5*80=1720 hz
    (note, high E on 5th string at fret 12 has a frequency of 659)
  extrema indices from autocorrelated data found
    (extremas should happen twice as the period of the fundamental)
  extrema indices, the value associated and their neighboring values passed into quad fit to get quadratic coefficients
  quadratic coefficients used to calculate sub-integer extrema location
  sub_integer extrema locations passed into averageGap
  calced_freq returned as 2*averageGap result
intended use for module
  initialize function that takes as an argument what power of 2 bins it uses
    defaults to 11
    sets a few module variables like bin width, the sound analyzer module
  getPitch function, takes no argument, returns best guess for fundamental or 0 for insufficient power
*/
