let processingPath;
// This will hold the last 5 elements (circles or paths).
let elementsQueue = [];

const sigProcName = 'signalProcessing'
if (window.location.href.includes("/pronunciationVis/")) {
    processingPath = `/pronunciationVis/${sigProcName}`; // Set for remote
} else {
    processingPath = "/"+sigProcName; // Set for local
}
/*
main colors for vowel chart
blue (L2)
light:      #ffffcc
between:    #a1dab4
med:        #41b6c4
between:    #2c7fb8
darkest:    #253494

orange (L1)
light:  #fc8d59
med:    #e34a33
dark:   #b30000
*/

"use strict";
window.addEventListener("load", drawVowelChart);
async function drawVowelChart(){
    const svg = d3.select("svg");
    const vwlChrtProperties = await svgGetPadding(svg);
    const paddingVwlChrt = vwlChrtProperties.padding;
    const svgWidth = vwlChrtProperties.width;
    const svgHeight = vwlChrtProperties.height;

   // define x boundaries of vowel chart
    const xPadding = paddingVwlChrt.x;
    const xWidth = svgWidth - 2*xPadding;
    const xfront = xPadding;
    const xnearFront = 0.125*xWidth + xPadding;
    const xmidFrontCent = 0.25*xWidth + xPadding;
    const xleftCent = 0.375*xWidth + xPadding;
    const xcent = 0.5*xWidth + xPadding;
    const xnearBack = 0.6875*xWidth + xPadding;
    const xback = xWidth + xPadding;

    // define y boundaries of vowel chart
    const yPadding = paddingVwlChrt.y;
    const yHeight = svgHeight - 2*yPadding;
    const yclose = yPadding;
    const ycloseMid = 0.3333*yHeight + yPadding;
    const yopenMid = 0.6666*yHeight + yPadding;
    const yopen = 0.9999*yHeight + yPadding;

    // send SVG properties to client
    // upper left, upper right, lower left, lower right
    const svgData = [[xfront,yclose],[xback,yclose],[xleftCent,yopen],[xback,yopen]];
    svgToClient(svgData);

    // Line properties
    const color = "#3a3a3a";
    const strokeOpacity = 0.90;
    const strokeLinecap = "round";
    const strokeWidth = 3;

    // Text properties
    const fontSize = "smaller";
    const fontFamily = "Courier, Helvetica, Verdana"

    // Text Labels
    const topText = 'high';
    const midTopText = 'med-high';
    const midBottomText = 'med-low';
    const bottomText = 'low';


    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // TEXT FOR VWL CHART
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // y labels
    const yAdjustAxis = 10
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xfront-10)
        .attr("text-anchor","end")
        .attr("y", yclose+yAdjustAxis)
        .text(topText);
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xnearFront-10)
        .attr("text-anchor","end")
        .attr("y", ycloseMid+10)
        .text(midTopText);
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xmidFrontCent-10)
        .attr("text-anchor","end")
        .attr("y", yopenMid)
        .text(midBottomText);
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xleftCent-10)
        .attr("text-anchor","end")
        .attr("y", yopen)
        .text(bottomText);

    // x labels
   svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xfront+10)
        .attr("text-anchor","end")
        .attr("y", yclose-10)
        .text("front");
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xcent)
        .attr("text-anchor","middle")
        .attr("y", yclose - 10)
        .text("central");
    svg.append("text")
        .attr("font-size",fontSize)
        .attr("font-family",fontFamily)
        .attr("x", xback)
        .attr("text-anchor","middle")
        .attr("y", yclose - 10)
        .text("back");

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // HORIZONTAL LINES FOR VWL CHART
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // create close line
    svg.append("line")
        .attr("x1", xfront)
        .attr("y1", yclose)
        .attr("x2", xback)
        .attr("y2", yclose)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);

    // create close-mid line
    svg.append("line")
        .attr("x1", xnearFront)
        .attr("y1", ycloseMid)
        .attr("x2", xback)
        .attr("y2", ycloseMid)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
    // create open-mid line
    svg.append("line")
        .attr("x1", xmidFrontCent)
        .attr("y1", yopenMid)
        .attr("x2", xback)
        .attr("y2", yopenMid)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
    // create open line
    svg.append("line")
        .attr("x1", xleftCent)
        .attr("y1", yopen)
        .attr("x2", xback)
        .attr("y2", yopen)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // VERTICAL LINES FOR VWL CHART
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // create front line
    svg.append("line")
        .attr("x1", xfront)
        .attr("y1", yclose)
        .attr("x2", xleftCent)
        .attr("y2", yopen)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
    // create central line
    svg.append("line")
        .attr("x1", xcent)
        .attr("y1", yclose)
        .attr("x2", xnearBack)
        .attr("y2", yopen)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
    // create back line
    svg.append("line")
        .attr("x1", xback)
        .attr("y1", yclose)
        .attr("x2", xback)
        .attr("y2", yopen)
        .attr("stroke", color)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-width", strokeWidth);
}

export async function drawVowels(dataL1Path) {
    // fetch json data
    const response1 = await fetch(dataL1Path);
    const dataL1 = await response1.json();
    const audioPath = dataL1Path.replace('.json', '.wav');

    const svg = d3.select("svg")
    const strokeLinecap = "round";
    const glideMakerL1 = d3.line()
        .x(d => d.x)
        .y(d => d.y)
        .curve(d3.curveCardinal);

    const colorSpa = 'green';
    const hoverColor = 'green';
    const strokeWidthDefault = 5;
    const strokeWidthHover = 8;

    // Define the color array
    const colors = ['#253494', '#2c7fb8', '#41b6c4', '#a1dab4', '#ffffcc']

    // Draw curves between related data points
    async function renderPaths() {
        // Push the new vowel data onto the queue
        // elementsQueue.push(uniqueId);
        const temp = audioPath.split('/')
        const uniqueId = temp[temp.length - 1].replaceAll('-','').replaceAll('_','').replace('.wav','')
        const markerId = `arrow-${uniqueId}`

        // add uniqueId to the beginning of the array
        elementsQueue.unshift(uniqueId)
        console.log(elementsQueue)
        console.log(uniqueId)

        // If we have more than 5 elements, remove the oldest one from the end
        if (elementsQueue.length > 5) {
            const oldestElementId = elementsQueue.pop();
            console.log(elementsQueue)
            console.log(oldestElementId)
            svg.select(`#${oldestElementId}`).remove();
        }


        for (let i = 0; i < dataL1.length; i++)  {
            const vowel = dataL1[i];
            if (Array.isArray(vowel.vwl) && vowel.vwl.length > 1) {
                // Create a unique marker for each path
                svg.append("defs").append("marker")
                    .attr("id", markerId)           // Changed to create a unique marker ID based on the loop index
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", 5)
                    .attr("markerWidth", 2)
                    .attr("markerHeight", 6)
                    .attr("orient", "auto")
                    .append("path")
                        .attr("d", "M0,-5L10,0L0,5")    // No change here
                        .attr("fill", colors[0]);

                const pathData = await Promise.all(vowel.vwl.map(async d => ({
                    x: await freqToSVG(d, 'x'),
                    y: await freqToSVG(d, 'y')
                })));
                svg.append("path")
                    .datum(pathData)
                    // .attr("id", uniqueId) // Add unique id to paths
                    .attr("id",uniqueId)
                    .attr('data-index', 0)  // Store the current index in the element's data
                    .attr("class", "vowel-shape") // Add this class to paths
                    .attr("fill", "none")
                    .attr("stroke", colors[0])
                    .attr("stroke-width", strokeWidthDefault)
                    .attr("stroke-linecap", strokeLinecap)
                    .attr("marker-end", `url(#${markerId})`)
                    // .attr("marker-end", `url(#arrow)`)
                    .attr("d", glideMakerL1)
                    .on('click', function () {
                        new Audio(audioPath).play();
                    })
                    .on("mouseover", function () {
                        d3.select(this)
                            .attr("stroke-width", strokeWidthHover)  // Increase stroke width on hover
                            .attr("stroke", hoverColor);   // Change stroke color on hover
                        // Change color of the arrowhead
                        d3.select(`#${markerId} path`)
                            .attr("fill", hoverColor);
                    })
                    .on("mouseout", function () {
                        let element = d3.select(this);
                        let index = element.attr('data-index');  // Retrieve the index from element's data
                        // Restore stroke width and color using the index
                        element.attr("stroke-width", strokeWidthDefault)
                               .attr('stroke', colors[index]);  // Use the index to get the original color

                        // Assuming the arrow is to be restored to the same color
                        d3.select(`#${markerId} path`).attr('fill',colors[index]);
                    });
            } else {
                // Draw individual points if no related data points found
                // Await the computation of x and y coordinates before appending the circle
                const coord = await Promise.resolve({
                    cx: await freqToSVG(vowel.vwl[0], 'x'),
                    cy: await freqToSVG(vowel.vwl[0], 'y')
                });
                svg.append("circle")
                    .data([coord])
                    .join("circle")
                    .attr("id", uniqueId) // Add unique id to paths
                    .attr("class", "vowel-shape") // Add this class to paths
                    .attr("cx", d => d.cx)
                    .attr("cy", d => d.cy)
                    .attr("r", strokeWidthDefault)
                    .attr("fill", color)
                    .on('click', function () {
                        new Audio(audioPath).play();
                    })
                    .on("mouseover", function () {
                        d3.select(this)
                            .attr("r", strokeWidthHover)  // Increase stroke width on hover
                            .attr("fill", hoverColor);   // Change stroke color on hover
                    })
                    .on("mouseout", function () {
                        d3.select(this)
                            .attr("r", strokeWidthDefault)  // Restore original stroke width
                            .attr('fill', color);
                    });
            }
        }
        // Update the colors of all elements
        console.log(elementsQueue)
        elementsQueue.forEach((id, index) => {
            svg.select(`#${id}`)
                .transition()
                .duration(500)
                .attr('data-index', index)  // Store the current index in the element's data
                // .attr('fill', colors[index])  // Set fill for circles
                .attr('stroke', colors[index]);  // Set stroke for paths
            d3.select(`#arrow-${id} path`).attr('fill',colors[index]);
        });
    }
    renderPaths();
}

async function svgGetPadding(svg) {
    // get height and width of svg
    const svgViewBox = svg.attr("viewBox").split(',');
    const svgXOrigin = svgViewBox[0];
    const svgYOrigin = svgViewBox[1];
    const svgWidth = svgViewBox[2];
    const svgHeight = svgViewBox[3];

    // Padding for vowel chart
    const fracOfWidth = 0.125;
    const fracOfHeight = 0.0625;
    const padding = {
        x:fracOfWidth*svgWidth,
        y:fracOfHeight*svgHeight
    };
    return {padding:padding,
        xOrigin:svgXOrigin,
        yOrigin:svgYOrigin,
        width:svgWidth,
        height:svgHeight};
}

async function svgToClient(data) {
    // fetch json data
    console.log(data)
    const urlPath = `${processingPath}/api/svgToConfig`
    const response = await fetch(urlPath, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify(data)
    });
}

async function freqToSVG(freq,axis){
    // fetch json data
    const urlPath = `${processingPath}/api/freqToSVG`
    const response = await fetch(urlPath, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify(freq)
    });
    const svg = await response.json();
    if (axis === 'x') {
        return svg.svg[0]
    }
    return svg.svg[1]
}
