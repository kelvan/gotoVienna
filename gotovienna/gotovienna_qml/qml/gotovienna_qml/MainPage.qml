import QtQuick 1.1
import com.nokia.meego 1.0
import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: commonTools

    TextField {
        placeholderText: 'origin'

        id: origin
        text: "Test"
        anchors {
            top: parent.top
            left: parent.left
            topMargin: 20
            leftMargin: 10
            rightMargin: 10
        }
        width: parent.width - 20
        //width: parent.width - anchors.leftMargin - anchors.rightMargin

         MouseArea {
             anchors.fill: parent
             drag.target: origin
             drag.axis: Drag.YAxis
             drag.minimumY: 0
             drag.maximumY: parent.height
         }
    }

    TextField {
        placeholderText: 'destination'
        id: destination
        anchors {
            top: origin.bottom
            left: parent.left
            right: parent.right
            topMargin: 10
            leftMargin: 10
            rightMargin: 10
        }
    }

    Button {
        id: btnSearch
        text: 'Search'
        anchors {
            top: destination.bottom
            topMargin: 10
            horizontalCenter: parent.horizontalCenter
        }
        onClicked: {
            console.debug("Origin: " + origin.text)
            console.debug("Destination: " + destination.text)
            pageStack.push(Qt.resolvedUrl("test.qml"))
        }
    }
}

