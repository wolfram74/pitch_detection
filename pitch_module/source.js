var PitchDetection = (function(){
  console.log('Pitch detector loaded')
  var API = {}
  API.mathUtil = (function(){
    var API = {}
    API.extremaFinder = function(array){
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

    API.autoCorrelation = function(array, maxShift){
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

    API.quadFit = function(x2, yvals){
      // returns a,b,c for ax**2+bx+c assuming y_vals come from points adjacent to x2
      a = (yvals[0] / 2.0) - yvals[1] + (yvals[2] / 2.0)
      b = x2*(
              2*yvals[1]-yvals[0]-yvals[2]
          ) - (
              yvals[0]-yvals[2]
          )*0.5
      c = x2*x2*(
              yvals[0]*0.5- yvals[1]+yvals[2]*0.5
          )+ x2*0.5*(
              yvals[0]-yvals[2]
          )+yvals[1]
      return [a, b, c]
    }

    API.averageGap = function(array){
      var total = array[0]
      for(var ind=1; ind<array.length; ind++){
        total += (array[ind]-array[ind-1])
      }
      return total/(array.length)
    }
    return API
  })()
  return API
})()
