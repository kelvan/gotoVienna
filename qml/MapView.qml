import QtQuick 1.1
import Qt 4.7
import QtMobility.location 1.2
import com.nokia.meego 1.0

Page {
    tools: mapTools

    ToolBarLayout {
        id: mapTools
        x: 0
        y: 0
        ToolIcon { iconId: "toolbar-back"; onClicked: { menu.close(); pageStack.pop(null,false); } }
    }

    Map {
        id: map
        plugin : Plugin {
            name : "nokia"
        }

        anchors.fill: parent
        size.width: parent.width
        size.height: parent.height
        zoomLevel: 7
        //center: positionSource.position.coordinate
        //objects: t_data.mapObjectsList


        onZoomLevelChanged: {
            console.log("Zoom changed")
        }

    }
}
