const check = "{{completed}}";
const cost = "{{final_cost}}";
const end = "{{end_time}}";


if (check) {
    cost.style.display = "block";
    end.style.display = "block";
}
else {
    cost.style.display = "none";
    end.style.display = "none";
}