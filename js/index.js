function main() {
    d3.json('data/data.json', function(data) {
        stream("#main", data);
    });
}

function stream(id, data) {
    // Get size of container and set some defaults.
    var width =  $(id).width() || 900;
    var height = $(id).height() || 600;

    // A few colors to mess with
    var color = d3.scale.category20b();

    var stack = d3.layout.stack()
            .offset("wiggle")
            .values(function(d) { return d.values; });

    var layers = stack(data);

    // Insert a new SVG element (our chart)
    var svg = d3.select(id)
            .append("svg")
            .attr("width", width)
            .attr("height", height);

    var x = d3.scale.linear()
            .domain([0, layers[0].values.length])
            .range([0, width]);

    var y = d3.scale.linear()
            .domain([0, d3.max(layers, function(layer) { return d3.max(layer.values, function(d) { return d.y0 + d.y; }); })])
            .range([0, height]);

    var area = d3.svg.area()
            .x(function(d, i) { return x(i); })
            .y0(function(d) { return y(d.y0); })
            .y1(function(d) { return y(d.y0 + d.y); });

    // tooltips
    svg.selectAll("path")
        .data(layers)
        .enter()
        .append("path")
        .style("fill", function(d, i) { return color(i);})
        .style("stroke", function(d, i) { return color(i);})
        .attr("d", function(d) { return area(d.values); })
        .append("title")
        .text(function(d) { return d.word; });
}
