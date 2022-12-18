function groupByInterval(tracks, target, intervalLength) {
    tracks = tracks.slice(-500);

    let artistScrobbles = {};
    const groups = new Map();

    let firstScrobbleTime = Date.parse(tracks[0]['time']);
    let currentIntervalStart = firstScrobbleTime - (firstScrobbleTime % intervalLength);

    tracks.forEach(track => {
        ts = Date.parse(track['time']);
        
        if (ts > currentIntervalStart + intervalLength){
            //add the artist scrobble numbers to the previous day
            groups.set(currentIntervalStart, artistScrobbles);

            //start tallying up scrobbles for the next interval
            currentIntervalStart += intervalLength;
            artistScrobbles = {};
        }

        artistScrobbles[track[target]] = (artistScrobbles[track[target]]+1) || 1 ;
    });
    
    groups.set(currentIntervalStart, artistScrobbles);
    return groups;
}

$(document).ready( function () {
    let tracks = JSON.parse(document.getElementById("timeline").dataset.tracks);
    
    /* 
        algorithm:
        - initially, or after resizing the window, determine maximum interval that fits at least once
        - for example: years > months > weeks > days > hour
    */
    let intervalLength = 1000 * 60 * 60 * 24;
    let days = groupByInterval(tracks, 'artist', intervalLength);

    let topArtists = []
    days.forEach((artists, day) => {
        topArtists.push({
            x: 'Most played artist',
            y: [
                day,
                day + intervalLength
            ],
        })
    })
    
    console.log(days);
    var options = {
        series: [ {data: topArtists} ],
        chart: {
            type: 'rangeBar'
        },
        plotOptions: {
            bar: {horizontal: true}
        },
        dataLabels: {
            enabled: true,
            formatter: function(vals, opts) {
                let artistScrobbles = days.get(vals[0])
                let topArtist = Object.keys(artistScrobbles).reduce(function(a, b){ return artistScrobbles[a] > artistScrobbles[b] ? a : b });
                
                return topArtist;
            }
        },
        xaxis: {
          type: 'datetime'
        }
    };

    var chart = new ApexCharts(document.querySelector("#timeline"), options);
    chart.render();

} );