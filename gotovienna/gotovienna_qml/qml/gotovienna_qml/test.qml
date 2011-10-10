import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    tools: commonTools

    Text {
        id: name
        font.pointSize: 30
        text: qsTr("Hello World")
    }

    PinchArea {
        anchors.fill: parent
        pinch.maximumScale: 10
        pinch.minimumScale: 1

        onPinchUpdated: {
            console.debug(pinch.scale)

        }

        onPinchFinished: {
            name.font.pointSize = name.font.pointSize * pinch.scale
        }
    }

}
