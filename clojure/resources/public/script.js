document.addEventListener("DOMContentLoaded", function () {
  const taskInput = document.getElementById("task-input");
  const addTaskButton = document.getElementById("add-task-button");
  const taskList = document.getElementById("task-list");

  function fetchTasks() {
    fetch("/api/tasks")
      .then((res) => res.json())
      .then((tasks) => {
        taskList.innerHTML = "";
        tasks.forEach((task, idx) => {
          const li = document.createElement("li");
          li.innerHTML = `
            <input type="checkbox" ${task.completed ? "checked" : ""} data-idx="${task.id}">
            <span style="text-decoration:${task.completed ? "line-through" : "none"}">${task.title}</span>
            <button data-del="${task.id}">Delete</button>
          `;
          taskList.appendChild(li);
        });
      });
  }

  addTaskButton.addEventListener("click", function () {
    const title = taskInput.value.trim();
    if (title) {
      fetch("/api/tasks", { 
        method: "POST",
        headers: {
          "content-type": "application/json"
        },
        body: JSON.stringify({
          title
        })
      })
        .then(() => {
          taskInput.value = "";
          fetchTasks();
        });
    }
  });

  taskList.addEventListener("click", function (e) {
    if (e.target.tagName === "BUTTON") {
      const idx = e.target.getAttribute("data-del");
      const url = "/api/tasks/" + idx;
      fetch(url, { method: "DELETE" })
        .then(fetchTasks);
    }
    if (e.target.tagName === "INPUT" && e.target.type === "checkbox") {
      const idx = e.target.getAttribute("data-idx");
      const url = "/api/tasks/" + idx;
      const completed = e.target.checked;
      fetch(url, {
        method: "PATCH",
        headers: {
          "content-type": "application/json"
        },
        body: JSON.stringify({
          completed
        })
      })
        .then(fetchTasks);
    }
  });

  fetchTasks();
});