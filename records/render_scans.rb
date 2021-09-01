require 'chunky_png'
=begin
need:
read files
color map from 0-255
formatting, give each bin a 2x2 pixel box
inbetween each time step put a 1 pixel seperator
100's [100,100,100]
50's [50,50,50]
10's [10,10,10]
else [0,0,0]
=end
def make_heat_map1()
  table = {}
  255.times do |n|
    norm = n.to_f/255
    r, g, b = (1-norm)*255, (norm)*(1-norm)*4*255, norm*255
    table[n]=[r.to_i, g.to_i, b.to_i]
  end
  table[0]=[25,25,25]
  table.default = [25,25,25]
  return table
end

# name = "2015-03-18T12/50/18-07/00.txt"
# name = "2015-03-18T12:50:18-07:00.txt"
=begin
2015-03-18T13/04/07-07/00
=end

name = "sample_5.txt"
file = File.open(name, 'r')
data = []
file.each do |line|
  data << line.split(",")
end
p data.length
p data[0].length
# p line_count
width = 3*data.length
height = (data[0].length-1)*2
heat_map = make_heat_map1()


pad_map = {10=>[250,50,50], 20=>[250,50,50], 30=>[250,50,50], 
  40=>[250,50,50], 60=>[250,50,50], 70=>[250,50,50], 
  80=>[250,50,50], 90=>[250,50,50],
  50=>[50,250,50], 0=>[255,255,255]}
pad_map.default = [0,0,0]
png =  ChunkyPNG::Image.new(width,height, ChunkyPNG::Color::TRANSPARENT)

data.length.times do |x|
    pad = pad_map[x%100]
    png.line(x*3,0,x*3,height-1, ChunkyPNG::Color.rgb(pad[0],pad[1],pad[2]))
  (data[0].length-1).times do |y|
    color = heat_map[data[x][y+1].to_i]
    # p data[x][y+1].to_i
    # p color
    rgb = ChunkyPNG::Color.rgb(color[0],color[1],color[2])
    # p rgb
    png[x*3+1, height-y*2-1] = rgb # ChunkyPNG::Color.rgb(color[0],color[1],color[2])
    png[x*3+2, height-y*2-1] = rgb # ChunkyPNG::Color.rgb(color[0],color[1],color[2])
    png[x*3+1, height-y*2-2] = rgb # ChunkyPNG::Color.rgb(color[0],color[1],color[2])
    png[x*3+2, height-y*2-2] = rgb # ChunkyPNG::Color.rgb(color[0],color[1],color[2])
  end
  p x
end

name[-3..-1]= 'png'
png.save(name , :interlace => true)
