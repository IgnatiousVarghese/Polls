

var data = {{ q_result.count| safe}};
var sum = 0;
for (let i = 0; i < data.length; i++) {
    sum += data[i];
}

var count_not_voted = {{ group.total_count| safe}} - sum;

var labels = {{ q_result.labels| safe}};
labels.push("None");
data.push(count_not_voted);

var color_list = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'
];

var l = labels.length - 1;
color_list[l] = 'grey'

var my_choice = "Your choice : {{q_result.my_vote|safe|escapejs}}";


var ctx = document.getElementById('myChart{{forloop.counter}}').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            label: '# of Votes',
            data: data,
            backgroundColor: color_list,
            borderColor: color_list,
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: my_choice
        }
    }
});