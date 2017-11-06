d3.json('data/nobel_winners.json', function(error, data){
    if(error){
        console.log(error);
    }
    d3.select('h2#data-title').text('All the Nobel-winners');
    d3.select('div#data pre').html(JSON.stringify(data, null, 4)); 
});


