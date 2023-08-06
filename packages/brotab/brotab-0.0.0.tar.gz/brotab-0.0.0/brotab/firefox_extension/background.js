/*
On startup, connect to the "firefox_mediator" app.
*/
var port = browser.runtime.connectNative("firefox_mediator");

// see https://stackoverflow.com/a/15479354/258421
function naturalCompare(a, b) {
    var ax = [], bx = [];

    a.replace(/(\d+)|(\D+)/g, function(_, $1, $2) { ax.push([$1 || Infinity, $2 || ""]) });
    b.replace(/(\d+)|(\D+)/g, function(_, $1, $2) { bx.push([$1 || Infinity, $2 || ""]) });

    while(ax.length && bx.length) {
        var an = ax.shift();
        var bn = bx.shift();
        var nn = (an[0] - bn[0]) || an[1].localeCompare(bn[1]);
        if(nn) return nn;
    }

    return ax.length - bx.length;
}

function listTabsSuccess(tabs) {
  lines = [];
  // Make sure tabs are sorted by their index within a window
  tabs.sort((a, b) => a.index > b.index);
  for (let tab of tabs) {
    line = tab.id + "\t" + tab.title + "\t" + tab.url;
    console.log(line);
    lines.push(line);
  }
  // lines = lines.sort(naturalCompare);
  port.postMessage(lines);
}

function listTabsError(error) {
  console.log(`Error: ${error}`);
}

function listTabs() {
  browser.tabs.query({}).then(listTabsSuccess, listTabsError);
}

function closeTabs(tab_ids) {
  browser.tabs.remove(tab_ids);
}

function moveTabs(move_pairs) {
  for (let pair of move_pairs) {
    browser.tabs.move(pair[0], {index: pair[1]}).then(
      (tab) => console.log(`Moved: ${tab}`),
      (error) => console.log(`Error moving tab: ${error}`)
    )
  }
}

function createTab(url) {
  browser.tabs.create({'url': url})
}

function activateTab(tab_id) {
  browser.tabs.update(tab_id, {'active': true})
}

/*
Listen for messages from the app.
*/
port.onMessage.addListener((command) => {
  console.log("Received: " + JSON.stringify(command, null, 4));

  if (command['name'] == 'list_tabs') {
    console.log('Listing tabs...');
    listTabs();
  }

  else if (command['name'] == 'close_tabs') {
    console.log('Closing tabs:', command['tab_ids']);
    closeTabs(command['tab_ids']);
  }

  else if (command['name'] == 'move_tabs') {
    console.log('Moving tabs:', command['move_pairs']);
    moveTabs(command['move_pairs']);
  }

  else if (command['name'] == 'new_tab') {
    console.log('Creating tab:', command['url']);
    createTab(command['url']);
  }

  else if (command['name'] == 'activate_tab') {
    console.log('Activating tab:', command['tab_id']);
    activateTab(command['tab_id']);
  }
});

/*
On a click on the browser action, send the app a message.
*/
// browser.browserAction.onClicked.addListener(() => {
//   // console.log("Sending:  ping");
//   // port.postMessage("ping");
//
//   console.log('Listing tabs');
//   listTabs();
// });
