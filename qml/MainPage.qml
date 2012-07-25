import QtQuick 1.1
import com.nokia.meego 1.0
import QtMobility.location 1.1

import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: commonTools
    orientationLock: PageOrientation.LockPortrait

    property bool canRefresh: realtimeResult.sourceUrl != '' || (realtimeResult.isStation && realtimeResult.gstation != '')
    property variant nearbyStations
    property string gline
    property string gstation

    function showFavorites() {
        favSelector.model.clear();
        for (var i=0; i<favManager.getCount(); i++) {
            var data = eval('(' + favManager.getItem(i) + ')');
            favSelector.model.append(data);
        }
        favSelector.model.sync();
        favSelector.open();
    }

    function search() {
        lineSheet.currentLine = '';
        lineSheet.open();
    }

    function refresh() {
        realtimeResult.refresh();
    }

    function fillNearbyStations(lat, lon) {
        nearbyStations = itip.get_nearby_stations(lat, lon);
    }

    function showNearby() {
        console.log("show nearby")

        var stations = nearbyStations;
        stationSelectorModel.clear();
        for (var idx in stations) {
            stationSelectorModel.append({'name': stations[idx]});
        }

        stationSelector.open();
    }

    Text {
        visible: !parent.canRefresh
        anchors.centerIn: parent
        font.pixelSize: 30
        text: '<p><strong>Welcome, traveller!<br></strong></p><p>Press <img src="image://theme/icon-m-toolbar-search"> to search for<br>departure information.</p><p>Press <img src="image://theme/icon-m-toolbar-view-menu"> for nearby stations.<br></p><p><strong>Have a safe journey.</strong></p>'
    }

    Rectangle {
        id: header
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
            margins: -1
        }
        border {
            color: 'black'
            width: 1
        }

        gradient: Gradient {
            GradientStop { position: 0; color: '#777' }
            GradientStop { position: 1; color: '#aaa' }
        }

        height: 80
        color: 'white'

        Image {
            id: logo
            source: 'logo.png'

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 10
            }
        }


        ToolIcon {
            property int increaseMeGently: 0
            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 10
            }
            platformIconId: {
                if (favManager.isFavorite(realtimeResult.gline, realtimeResult.gdirection, realtimeResult.gstation, realtimeResult.sourceUrl, realtimeResult.isStation, increaseMeGently)) {
                    'icon-m-toolbar-favorite-mark'
                } else {
                    'icon-m-toolbar-favorite-unmark'
                }
            }
            onClicked: {
                favManager.toggleFavorite(realtimeResult.gline, realtimeResult.gdirection, realtimeResult.gstation, realtimeResult.sourceUrl, realtimeResult.isStation);
                increaseMeGently = increaseMeGently + 1;
            }
        }
    }

    PositionSource {
        id: positionSource
        updateInterval: 10000

        active: true

        onPositionChanged: {
            fillNearbyStations(positionSource.position.coordinate.latitude, positionSource.position.coordinate.longitude)
        }
    }

    SelectionDialog {
        id: stationSelector
        titleText: 'Select nearby station'

        model: ListModel {
            id: stationSelectorModel
        }

        onAccepted: {
            realtimeResult.isStation = true
            realtimeResult.gline = ''
            realtimeResult.sourceUrl = ''
            gline.text = ''
            gstation = stationSelectorModel.get(selectedIndex).name
            realtimeResult.gstation = stationSelectorModel.get(selectedIndex).name
            console.log('station to get: ' + realtimeResult.gstation)
        }
    }

    LineSheet {
        id: lineSheet
        onAccepted: {
            gline = currentLine

            /* We usually want to select a station after selecting a line */
            stationSheet.open();
            stationSheet.loadData(gline);
        }
    }

    StationSheet {
        id: stationSheet
        onAccepted: {
            gstation.text = stationSheet.currentStation

            realtimeResult.gline = stationSheet.currentLine
            realtimeResult.gdirection = stationSheet.currentDirection
            realtimeResult.isStation = false
            realtimeResult.sourceUrl = itip.get_directions_url(stationSheet.currentLine, stationSheet.currentDirection, stationSheet.currentStation)
            realtimeResult.gstation = stationSheet.currentStation

            console.debug('url to get: ' + realtimeResult.sourceUrl)
            realtimeResult.refresh()
        }
    }

    ResultRealtime {
        id: realtimeResult

        anchors {
            margins: 10
            top: header.bottom
            left: parent.left
            bottom: parent.bottom
            right: parent.right
        }

        clip: true

        gline: stationSheet.currentLine
        gstation: stationSheet.currentStation
        gdirection: stationSheet.currentDirection

        sourceUrl: stationSheet.currentUrl
    }

    SelectionDialog {
        id: favSelector
        titleText: 'Your favorites'

        model: ListModel {}

        onAccepted: {
            realtimeResult.isStation = model.get(selectedIndex).isstation
            realtimeResult.gline = model.get(selectedIndex).gline
            realtimeResult.gdirection = model.get(selectedIndex).gdirection
            realtimeResult.sourceUrl = model.get(selectedIndex).sourceurl
            realtimeResult.gstation = model.get(selectedIndex).gstation
            realtimeResult.refresh()
        }
    }
}

