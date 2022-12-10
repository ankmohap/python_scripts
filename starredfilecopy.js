function getSubFolders(parent) {
  var destination = DriveApp.getFolderById("ADD DESITINATION FOLDER");
  parent = parent.getId();
  var childFolder = DriveApp.getFolderById(parent).getFolders();
  while(childFolder.hasNext()) {
    var child = childFolder.next();
    Logger.log(child.getName());
    getSubFolders(child); 
    var files = child.getFiles();
  while (files.hasNext()){
    var file = files.next();
    //Logger.log(file.getName());
    if (file.isStarred()){
      Logger.log("STARRED----->"+file.getName());
      file.makeCopy(destination);
    }
  }
  }
  return;
}

function listFolders() {
  var parentFolder = DriveApp.getFolderById("ADD SOURCE FOLDER");
  var childFolders = parentFolder.getFolders();
  while(childFolders.hasNext()) {
    var child = childFolders.next();
    Logger.log(child.getName());
    getSubFolders(child);
  }
}
