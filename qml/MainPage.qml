import QtQuick 1.1
import com.nokia.meego 1.0
import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: commonTools

    Image {
        id: logo
        source: 'logo.png'

        anchors {
            topMargin: 25
            top: parent.top
            horizontalCenter: parent.horizontalCenter
        }
    }

    TextField {
        placeholderText: 'Line'

        id: gline
        anchors {
            top: logo.bottom
            left: parent.left
            topMargin: 20
            leftMargin: 10
            rightMargin: 10
        }
        width: parent.width - 20

         MouseArea {
             anchors.fill: parent
             drag.target: gline
             drag.axis: Drag.YAxis
             drag.minimumY: 0
             drag.maximumY: parent.height
         }
    }

    TextField {
        placeholderText: 'Station'
        id: gstation
        anchors {
            top: gline.bottom
            left: parent.left
            right: parent.right
            topMargin: 10
            leftMargin: 10
            rightMargin: 10
        }
    }

    ResultRealtime { id: resu }

    Button {
        id: btnSearch
        text: 'Search'
        anchors {
            top: gstation.bottom
            topMargin: 10
            horizontalCenter: parent.horizontalCenter
        }
        onClicked: {
            resu.gline = gline.text
            resu.gstation = gstation.text
            pageStack.push(resu)
            itip.search(gline.text, gstation.text)
            resu.busy = false
        }
    }
}

