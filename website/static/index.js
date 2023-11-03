function deleteProject(projectId) {
  fetch("/delete-project", {
    method: "POST",
    body: JSON.stringify({ projectId: projectId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function addMember(projectId, member) {
  fetch("/add-member", {
    method: "POST",
    body: JSON.stringify({ 
      projectId: projectId, 
      member: member
    }),
  }).then((_res) => {
    window.location.href = "/";
  });
  console.log("addMember success?")
}
