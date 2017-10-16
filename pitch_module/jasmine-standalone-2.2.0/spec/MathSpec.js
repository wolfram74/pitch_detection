describe("Meta", function() {

  beforeEach(function() {
  });

  it("should be able to run tests", function() {
    expect(true).toEqual(true);
  });
});

describe('Math utilities', function(){
  describe('Extrema finder', function(){
    it('should find maxima', function(){
      var curve = [0,1,2,3,4,5,6,5,4,3,2,3,4]
      var extremas = PitchDetection.mathUtil.extremaFinder(curve)
      expect(extremas).toEqual([6,10])
    })
  })
  describe('quadratic fitter', function(){
    it('it should fit 3 even spaced data points to a quadratic curve', function(){
      var yvals = [3,7,-2]
      for(var center = 1; center<11; center++){
        var params = PitchDetection.mathUtil.quadFit(center, yvals)
        var calced = [
          params[0]*(center-1)*(center-1)+params[1]*(center-1)+params[2],
          params[0]*(center)*(center)+params[1]*(center)+params[2],
          params[0]*(center+1)*(center+1)+params[1]*(center+1)+params[2]
        ]
        expect(calced).toEqual(yvals)
      }
    })
  })
  describe('Extrema Fitter', function(){
    it('should take extrema and find their implied position', function(){
      var curve = [0, 2, 1,0,3];
      var extremas = PitchDetection.mathUtil.extremaFinder(curve);
      expect(extremas).toEqual([1,3])
      var fitExtrema = PitchDetection.mathUtil.fitExtrema(extremas, curve);
      expect(fitExtrema[0]<fitExtrema[1]).toEqual(true)
      expect(fitExtrema[0]).not.toEqual(extremas[0])
    })
  })
  describe('Auto Correlation', function(){
    it('it should calcuate Auto Correlation to some extent',function(){
      var curve = [3,-2,1,-4,2]
      var autoCor = PitchDetection.mathUtil.autoCorrelation(curve, 3)
      expect(autoCor).toEqual([34, -14, -3])
    })
  })
  describe('average gap',function(){
    it('should calculate the average gap between values', function(){
      var values = [1.5, 3, 4.5, 6, 7.5]
      expect(PitchDetection.mathUtil.averageGap(values)).toEqual(1.5)
    })
  })
  describe('detrender', function(){
    it('should reduce contribution of linear trends', function(){
      var data= []
      var slope = -0.10;
      var b = 2000
      for(var index= 0; index<1000; index++){
        data.push(b+slope*index+Math.cos(index/10))
      };
      var rawArea = data.reduce((a,b)=>{return a+b})
      var detrended = PitchDetection.mathUtil.detrender(data, 80);
      var detArea = detrended.reduce((a,b)=>{return a+b})
      console.log(rawArea, detArea, detArea/rawArea)
      expect(rawArea>detArea).toEqual(true)
    })
  })
})
