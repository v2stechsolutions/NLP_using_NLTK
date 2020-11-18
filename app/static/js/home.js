$('.enteredTextDivision').hide();
$('.sentimentalAnalysisDivision').hide();
$('.mainTopicsDivision').hide();

function submitEnteredText(){
    text = $('#textForAnalysis').val()
    if(text == ''){
        alert('Please enter text for analysis.')
    }
    else{
        submitEnteredTextFunction()
    }
}

function submitEnteredTextFunction(){
    text = $('#textForAnalysis').val()
    content ={
        text : text
    }
    $.ajax({
        method: 'POST',
        data: JSON.stringify(content),
        contentType: 'application/json',
        dataType: 'text',
        url : 'predict',
        async : true,
        
        success: function(jsonData){
            if(jsonData){
                // console.log(jsonData)
                // console.log(typeof(jsonData))
                // console.log(JSON.parse(jsonData))
                // console.log(typeof(JSON.parse(jsonData)))
                jsonData = JSON.parse(jsonData)
                console.log(jsonData)
                console.log(jsonData[0])
                console.log(jsonData[1])
                $('.sentimentAnalysis').text(jsonData[0].classifier);
                $('.enterdText').text(text)
                $(".mainTopics").empty();

                // $('.mainTopics').text(jsonData[1].topics)
                // alert(jsonData[1].topics.length)

                for(i=0; i <= (jsonData[1].topics.length) - 1;i++){
                    temp = '<p style="color:white">'+jsonData[1].topics[i]+'</p>'
                    $(".mainTopics").append(temp);
                }
                
                $("#textForAnalysis").val('');
                $('.enteredTextDivision').show();
                $('.sentimentalAnalysisDivision').show();
                $('.mainTopicsDivision').show();
                
            }
            else{
                console.log(jsonData)
            }
        },
        error: function(error, xhr, status) {
                alert('error')
            }
    });
    }
