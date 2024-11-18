


jsPsych.plugins['assignment-inference'] = (function() {
  var plugin = {};

  plugin.info = {
    name: 'assignment-inference',
    description: 'assignment-inference plugin',
    parameters: {
   label_options: {
        type: jsPsych.plugins.parameterType.STRING,
        array: true,
        pretty_name: 'Concept List',
        default: null,
        description: 'The options'
      },
      answer_key: {
        type: jsPsych.plugins.parameterType.STRING,
        array: true,
        pretty_name: 'Answer List',
        default: null,
        description: 'Correct labels'
      },
    bar_cols: {
        type: jsPsych.plugins.parameterType.STRING,
        array: true,
        pretty_name: 'list of bar colors',
        default: null,
        description: 'The colors of the bars'
      },
    color_cond: {
        type: jsPsych.plugins.parameterType.STRING,
        array: false,
        pretty_name: 'colorabity',
        default: null,
        description: 'colorabity condition: colorable or not'
      },
    category: {
        type: jsPsych.plugins.parameterType.STRING,
        array: false,
        pretty_name: 'concept category',
        default: null,
        description: 'which concept category'
      },
    repetition: {
        type: jsPsych.plugins.parameterType.INT,
        array: false,
        pretty_name: 'repetition number',
        default: null,
        description: 'Repetition number'
      },
      order_num:{
        type: jsPsych.plugins.parameterType.INT,
        array: false,
        pretty_name: 'latin square number',
        default: null,
        description: 'latin squre number'
      },
   pal_source: {
    type: jsPsych.plugins.parameterType.STRING,
    array: false,
    pretty_name: 'palette source',
    default: null,
    description: 'source of palette: UW71 or Tableau20'
  },

   instructions: {
    type: jsPsych.plugins.parameterType.BOOLEAN,
    array: false,
    pretty_name: 'Instructions',
    default: null,
    description: 'Show instructions?'
  },
}
}

plugin.trial = function(display_element,trial){
display_element.innerHTML='';

if(trial.instructions==true){
  var zoomScale= 0.6;
  window.zoomScale = 0.6;
  var modified =('<div class ="big cont" style="position:relative;height:800px; margin-top 0px;"><div><p style="text-align:left;margin-right:auto;margin-left:auto;width:900px">.\
    <br>Again, your task is to match each label to its corresponding bar color by clicking on the label, and dragging it to the box below the bar.\
   If you are unsure how to match the labels to the bar colors, use your best guess.<br>You can reset all the labels back to the top of the bars with the "Reset labels" button. Familiarize yourself with the interface by labeling all the bars below.<br> \
   <br>When you are ready to begin the experiment press the "Begin" button on the upper right.</p></div>')

  //var test =('<div class= "test" style="position:relative"><div style="position:relative">TEXT</div> ')
  modified+=('<DIV id = "containment-wrapper" style="transform:scale(0.6,0.6); transform-origin: top center;">\
<div id = "concept-container", style="position:relative; background: #595959; height: 250px; margin-bottom: 10px; text-align: center;margin-top: 10px" > \
     <div class = "concept-option" style="color: black; margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border:1px solid black; cursor: grab;line-height:50px; font-size: 22px"><p style= "z-index:3" ></p></div>\
     <div class = "concept-option" style="color: black;margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border: 1px solid black;cursor: grab;line-height:50px;font-size: 22px"><p style= "z-index:3"></p></div>\
     <div class = "concept-option" style="color: black;margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border: 1px solid black;cursor: grab;line-height:50px;font-size: 22px"><p style= "z-index:3"></p></div>\
     <div class = "concept-option" style="color: black;margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border:1px solid black;cursor: grab;line-height:50px;font-size: 22px"><p style= "z-index:3"></p></div>\
      </div><div id ="button-container" style="margin-left:auto;margin-right:auto;width:850px;height:20px;margin-bottom: 100px;background: #595959">\
<button id="reset" style="float:left; height: 40px;background-color: #ddd;border-color: #ccc;border-radius: 5px;">Reset labels</button>\
<button id="end_trial" style="float:right; height: 40px;border-radius: 5px;">Begin</button>\
</div>\
<div class="canvas-container", style="position:relative; height:300px;width:800px;margin-left:auto;margin-right: auto;  margin-top: 5px;background: #595959">\
<canvas id="myChart", style="z-index: 1;\
height: 100%;\
width:85%;\
margin-left:auto;margin-right: auto;\
/*margin-left:45%;*/\
top:0px;\
"></canvas>\
</div>\
<div id = "concept-sink" style="position:relative; background: #595959; height: 60px;width:800px;margin-left:auto;\
margin-right: auto; "> \
<div class = "something" style="background: #595959; margin-left:auto;margin-right:auto;margin-top:10px;height:100px;width:90%;overflow: hidden;">\
  <div class = "concept-receiver" style=" position:relative; display: inline-block;background: #595959; width:120px;height:60px;text-align: center;margin-top: 5px; margin-left: 5x; margin-right: 7px; border: 1px solid black;line-height:60px" draggable= "true"><p style="color: #595959;text-align: center; font-size: 22px"> ____ </p></div>\
  <div  class = "concept-receiver" style=" position:relative; display: inline-block; background: #595959;width:140px;height:60px ;text-align: center;margin-top: 5px;margin-left: 7px; margin-right: 7px; border: 1px solid black; line-height:60px" draggable= "true"><p style="color: #595959;text-align: center ; font-size: 22px">____</p></div>\
  <div class = "concept-receiver" style=" position:relative; display: inline-block;; background: #595959;width:140px;height:60px ;text-align: center;margin-top: 5px;margin-left: 7px; margin-right: 7px; border: 1px solid black;line-height:60px" draggable= "true"><p style="color: #595959;text-align: center; font-size: 22px">____</p></div>\
  <div class = "concept-receiver" style=" position:relative; display: inline-block; background: #595959;width:140px;height:60px ;text-align: center;margin-top: 5px;margin-left: 7px; margin-right: 7px; border: 1px solid black;line-height:60px" draggable= "true"><p style="color: #595959;text-align: center; font-size: 22px">____</p></div>\
</div></div></DIV></div>')
//  display_element.innerHTML+=('</div>')
display_element.innerHTML=modified;

}else{

  var zoomScale=1;
  window.zoomScale = 1;

display_element.innerHTML+=('<DIV id = "containment-wrapper">\
<div id = "concept-container", style="position:relative; background: #595959; height: 250px; margin-bottom: 10px; text-align: center;margin-top: 10px" > \
     <div class = "concept-option" style="color: black; margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border:1px solid black; cursor: grab;line-height:50px; font-size: 22px"><p style= "z-index:3" ></p></div>\
     <div class = "concept-option" style="color: black;margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border: 1px solid black;cursor: grab;line-height:50px;font-size: 22px"><p style= "z-index:3"></p></div>\
     <div class = "concept-option" style="color: black;margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border: 1px solid black;cursor: grab;line-height:50px;font-size: 22px"><p style= "z-index:3"></p></div>\
     <div class = "concept-option" style="color: black;margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border:1px solid black;cursor: grab;line-height:50px;font-size: 22px"><p style= "z-index:3"></p></div>\
      </div><div id ="button-container" style="margin-left:auto;margin-right:auto;width:850px;height:20px;margin-bottom: 100px;background: #595959">\
<button id="reset" style="float:left; height: 40px;background-color: #ddd;border-color: #ccc;border-radius: 5px;">Reset labels</button>\
<button id="end_trial" style="float:right; height: 40px;border-color: #ccc;border-radius: 5px;">Done</button>\
</div>\
<div class="canvas-container", style="position:relative; height:300px;width:800px;margin-left:auto;margin-right: auto;  margin-top: 5px;background: #595959">\
<canvas id="myChart", style="z-index: 1;\
height: 100%;\
width:85%;\
margin-left:auto;margin-right: auto;\
/*margin-left:45%;*/\
top:0px;\
"></canvas>\
</div>\
<div id = "concept-sink" style="position:relative; background: #595959; height: 60px;width:800px;margin-left:auto;\
margin-right: auto; "> \
<div class = "something" style="background: #595959; margin-left:auto;margin-right:auto;margin-top:10px;height:100px;width:90%;overflow: hidden;">\
  <div class = "concept-receiver" style=" position:relative; display: inline-block;background: #595959; width:140px;height:60px;text-align: center;margin-top: 5px; margin-left: 5x; margin-right: 7px; border: 1px solid black;line-height:60px" draggable= "true"><p style="color: #595959;text-align: center; font-size: 22px"> ____ </p></div>\
  <div  class = "concept-receiver" style=" position:relative; display: inline-block; background: #595959;width:140px;height:60px ;text-align: center;margin-top: 5px;margin-left: 7px; margin-right: 7px; border: 1px solid black; line-height:60px" draggable= "true"><p style="color: #595959;text-align: center ; font-size: 22px">____</p></div>\
  <div class = "concept-receiver" style=" position:relative; display: inline-block;; background: #595959;width:140px;height:60px ;text-align: center;margin-top: 5px;margin-left: 7px; margin-right: 7px; border: 1px solid black;line-height:60px" draggable= "true"><p style="color: #595959;text-align: center; font-size: 22px">____</p></div>\
  <div class = "concept-receiver" style=" position:relative; display: inline-block; background: #595959;width:140px;height:60px ;text-align: center;margin-top: 5px;margin-left: 7px; margin-right: 7px; border: 1px solid black;line-height:60px" draggable= "true"><p style="color: #595959;text-align: center; font-size: 22px">____</p></div>\
</div></div></DIV>')}


var start_time = (new Date()).getTime();




//initialize variables

var labeled_count = 0;
var concept_tracker =[]


//define functions

var end_trial = function(results) {

	 var elements = $('.concept-receiver p');
    var responses = []

    _.forEach(elements, function(p){
        responses.push(p.innerHTML)
       })

    var time = Date.now();

    res = checkAnswers(responses,answer_key)


var end_time = (new Date()).getTime();
var rt= end_time - start_time; 

// var turkInfo = jsPsych.turk.turkInfo();
   var trial_data = {
    'rt': rt,     
    'label_options':JSON.stringify(trial.label_options),
	'bar_cols': JSON.stringify(trial.bar_cols),
	'answer_key':JSON.stringify(trial.answer_key),
	'label_responses' : JSON.stringify(responses), 
	'condition':JSON.stringify(trial.color_cond),
	'repetition' :JSON.stringify(trial.repetition),
	'category' :JSON.stringify(trial.category),
	'pal_source': JSON.stringify(trial.pal_source),
	'accuracies': JSON.stringify(res),
	'total accuracy':JSON.stringify(res.reduce((a, b) => a + b, 0)),
	'order_num':JSON.stringify(trial.order_num)

   };

   console.log(trial_data);



   // clear the display
   display_element.innerHTML = '';

  // move on to the next trial
  jsPsych.finishTrial(trial_data);
    };



$('#end_trial').prop('disabled',true) 


function getRandNum(base, max, min){

   return (base + Math.round(Math.random() * (max - min) + min))
}



function checkAnswers(a, b) {
  answer_log=[] 
  if (a.length !== b.length) return false;

  // If you don't care about the order of the elements inside
  // the array, you should sort both arrays here.
  // Please note that calling sort on an array will modify that array.
  // you might want to clone your array first.

  for(i=0;i<a.length;i++){
    if(a[i]==b[i]){
        answer_log.push(1)

    }else{
        answer_log.push(0)
    }

    
  }

return answer_log;
}


//label_options = ["Sandstorm","Efficiency","Blizzard","Hurricane","Reliability"]

label_options  = trial.label_options
//answer_key = ["Hurricane","Sandstorm","Blizzard","Efficiency","Reliability"]
answer_key = trial.answer_key;


 var option_divs = $('.concept-option').find('p');

 if(trial.instructions==true){
 for(i=0;i<4;i++){
   option_divs[i].innerHTML=label_options[i];
}
 }else{
  for(i=0;i<4;i++){
    option_divs[i].innerHTML=label_options[i];
  }}


    $( ".concept-option" ).find('p').draggable({


       start: function(event, ui) {
        ui.position.left = 0;
        ui.position.top = 0;
    },
    drag: function(event, ui) {

        var changeLeft = ui.position.left - ui.originalPosition.left; // find change in left
        var newLeft = ui.originalPosition.left + changeLeft / (( zoomScale)); // adjust new left by our zoomScale

        var changeTop = ui.position.top - ui.originalPosition.top; // find change in top
        var newTop = ui.originalPosition.top + changeTop / zoomScale; // adjust new top by our zoomScale

        ui.position.left = newLeft;
        ui.position.top = newTop;

    },
      //helper: "clone",
    revert: "invalid",
     scroll: false 
});
    $( ".concept-option" ).find('p').css("z-index","3");


  $( ".concept-receiver" ).droppable({
    drop:  function( event, ui ) {
        concept_tracker.push(ui.draggable[0].innerHTML)
        labeled_count++
        //ui.droppable('enable');

        var dobj = $(this)
        $( this )
            .droppable('disable')
            .html('<p style="color: black;text-align: center; font-size: 22px;z-index:3">'+ui.draggable[0].innerHTML+'</p>')
            .find('p').draggable({


              start: function(event, ui) {
        ui.position.left = 0;
        ui.position.top = 0;
    },
    drag: function(event, ui) {

        var changeLeft = ui.position.left - ui.originalPosition.left; // find change in left
        var newLeft = ui.originalPosition.left + changeLeft / (( zoomScale)); // adjust new left by our zoomScale

        var changeTop = ui.position.top - ui.originalPosition.top; // find change in top
        var newTop = ui.originalPosition.top + changeTop / zoomScale; // adjust new top by our zoomScale

        ui.position.left = newLeft;
        ui.position.top = newTop;
        dobj.droppable('enable')

    },
              
              //revert: function(){dobj.droppable('disable'); return "invalid"},
  

              revert: function(droppableObj) {
                                 //if false then no socket object drop occurred.
                                 if(droppableObj === false)
                                 {
                                    dobj.droppable('disable')
                                    //revert the .myselector object by returning true
                                    return true;
                                 }
                                 else
                                 {
                                  
                                    return false;
                                 }
                              },

                             
            
              scroll: false 
              });

              $( ".concept-option" ).css("z-index","1");




            console.log(ui.draggable[0].outerHTML)
            ui.draggable[0].outerHTML = '<p style="color: #595959;text-align: center; font-size: 22px"> ____ </p>';
          
    
            if(trial.instructions==true){
              $('#end_trial').prop('disabled',!(_.uniq(concept_tracker).length==4))
              }else{
              $('#end_trial').prop('disabled',!(_.uniq(concept_tracker).length==4))
              }
  


              
      }
}
);


$("#end_trial").click(function(){end_trial()})


$("#reset").click(function() {
    $('#end_trial').prop('disabled',true) 
    labeled_count=0;
    concept_tracker =[]

    $('#concept-container').empty();
    //$('.concept-receiver').empty();
    $('.concept-receiver').find('p').replaceWith('____');
    $('.concept-receiver').css('color', '#595959');
    $('.concept-receiver').css('font-size', '22px');
    $('.concept-receiver').droppable('enable');
   

$( ".concept-receiver" ).droppable({
    drop:  function( event, ui ) {
        concept_tracker.push(ui.draggable[0].innerHTML)
        labeled_count++
        //ui.droppable('enable');

        var dobj = $(this)
        $( this )
            .droppable('disable')
            .html('<p style="color: black;text-align: center; font-size: 22px;z-index:3">'+ui.draggable[0].innerHTML+'</p>')
            .find('p').draggable({

               start: function(event, ui) {
        ui.position.left = 0;
        ui.position.top = 0;
    },
    drag: function(event, ui) {

        var changeLeft = ui.position.left - ui.originalPosition.left; // find change in left
        var newLeft = ui.originalPosition.left + changeLeft / (( zoomScale)); // adjust new left by our zoomScale

        var changeTop = ui.position.top - ui.originalPosition.top; // find change in top
        var newTop = ui.originalPosition.top + changeTop / zoomScale; // adjust new top by our zoomScale

        ui.position.left = newLeft;
        ui.position.top = newTop;
        dobj.droppable('enable')

    },
              
              //revert: function(){dobj.droppable('disable'); return "invalid"},
              //drag: function(event,ui){ dobj.droppable('enable')},

              revert: function(droppableObj) {
                                 //if false then no socket object drop occurred.
                                 if(droppableObj === false)
                                 {
                                    dobj.droppable('disable')
                                    //revert the .myselector object by returning true
                                    return true;
                                 }
                                 else
                                 {
                                  
                                    return false;
                                 }
                              },

                             
            
              scroll: false 
              });

              $( ".concept-option" ).css("z-index","1");




            console.log(ui.draggable[0].outerHTML)
            ui.draggable[0].outerHTML = '<p style="color: #595959;text-align: center; font-size: 22px"> ____ </p>';
            console.log(ui.draggable[0].outerHTML)
            if(trial.instructions==true){
            $('#end_trial').prop('disabled',!(_.uniq(concept_tracker).length==4))
            }else{
            $('#end_trial').prop('disabled',!(_.uniq(concept_tracker).length==4))
            }


              
      }
});






if(trial.instructions==true){
    for(i=0;i<4;i++){
    div_text  = '<div class = "concept-option" style="color: black; margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border:1px solid black; cursor: grab;line-height:50px; font-size: 22px"><p style= "z-index:3" >'+label_options[i]+'</p></div>'

    $('#concept-container').append(div_text);
}}else{
  for(i=0;i<4;i++){
    div_text  = '<div class = "concept-option" style="color: black; margin-left:auto;margin-right:auto;width:120px;height:50px;background: #595959;margin-bottom: 5px;border:1px solid black; cursor: grab;line-height:50px; font-size: 22px"><p style= "z-index:3" >'+label_options[i]+'</p></div>'

    $('#concept-container').append(div_text);
}

}

    $( ".concept-option" ).find('p').draggable({
        start: function(event, ui) {
        ui.position.left = 0;
        ui.position.top = 0;
    },
    drag: function(event, ui) {

        var changeLeft = ui.position.left - ui.originalPosition.left; // find change in left
        var newLeft = ui.originalPosition.left + changeLeft / (( zoomScale)); // adjust new left by our zoomScale

        var changeTop = ui.position.top - ui.originalPosition.top; // find change in top
        var newTop = ui.originalPosition.top + changeTop / zoomScale; // adjust new top by our zoomScale

        ui.position.left = newLeft;
        ui.position.top = newTop;

    },
      //helper: "clone",
    revert: "invalid",
     scroll: false 
});
    $( ".concept-option" ).find('p').css("z-index","3");


});

if(trial.instructions==true){
var barHeights =  _.times(4,function(){return getRandNum(13,2,-2)})
}else{
var barHeights =  _.times(4,function(){return getRandNum(13,2,-2)})
}

//listoflists.push( [12, 19, 15, 13, 13, 8])

var ctx = document.getElementById('myChart').getContext('2d');
ctx.canvas.width  =800;
ctx.canvas.height = 400;

// var ctx2 = document.getElementById('myChart2').getContext('2d');
// ctx2.canvas.width  = 800;
// ctx2.canvas.height = 500;

if(trial.instructions==true){

var myChart = new Chart(ctx, {

    type: 'bar',
    data: {
        labels: ['Contept 1', 'Contept 2', 'Contept 3', 'Contept 4' ],
        datasets: [{
            data: barHeights,
            backgroundColor: [
            trial.bar_cols[0],
            trial.bar_cols[1],
            trial.bar_cols[2],
            trial.bar_cols[3],
            // trial.bar_cols[4],
            ],
            borderColor: [
            trial.bar_cols[0],
            trial.bar_cols[1],
            trial.bar_cols[2],
            // trial.bar_cols[3],
            trial.bar_cols[4],
            ],
            borderWidth: 1,

            barThickness: 130,
            categoryPercentage:1,
            borderSkipped:'bottom'
        }]
    },
    options: {
        responsive: false,
        legend:{display: false},
        animation: {duration: 0},
        tooltips: {enabled: false},
        hover: {mode: null},
        scales: {
            yAxes: [{
                 gridLines: {display: true,
                 drawBorder: true,
                 drawOnChartArea: false,
                 lineWidth:2,
                 color: '#000000',
                 tickMarkLength: 0
                    },
                ticks: {
                    display: false,
                    beginAtZero: true,
                    padding: 100
                }
            }],
            xAxes:[{ gridLines: {display: true,
            drawBorder: true,
            drawOnChartArea: false,
            lineWidth:1,
            color: '#000000'
            },
            ticks:{display: false}}]
        }
    }
})}else{




var myChart = new Chart(ctx, {

  type: 'bar',
  data: {
      labels: ['Contept 1', 'Contept 2', 'Contept 3', 'Contept 4'],
      datasets: [{
          data: barHeights,
          backgroundColor: [
          trial.bar_cols[0],
          trial.bar_cols[1],
          trial.bar_cols[2],
          trial.bar_cols[3],

          ],
          borderColor: [
          trial.bar_cols[0],
          trial.bar_cols[1],
          trial.bar_cols[2],
          trial.bar_cols[3],
 
          ],
          borderWidth: 1,

          barThickness: 130,
          categoryPercentage:1,
          borderSkipped:'bottom'
      }]
  },
  options: {
      responsive: false,
      legend:{display: false},
      animation: {duration: 0},
      tooltips: {enabled: false},
      hover: {mode: null},
      scales: {
          yAxes: [{
               gridLines: {display: true,
               drawBorder: true,
               drawOnChartArea: false,
               lineWidth:2,
               color: '#000000',
               tickMarkLength: 0
                  },
              ticks: {
                  display: false,
                  beginAtZero: true,
                  padding: 100
              }
          }],
          xAxes:[{ gridLines: {display: true,
          drawBorder: true,
          drawOnChartArea: false,
          lineWidth:1,
          color: '#000000'
          },
          ticks:{display: false}}]
      }
  }
})
}





}
  return plugin;
})();
