
import QtQuick 1.1
import com.nokia.meego 1.0

Sheet {
    id: lineSheet
    property alias currentLine: linePad.currentLine

    acceptButtonText: 'Select'
    rejectButtonText: 'Cancel'

    content: LinePad {
        id: linePad
        anchors.fill: parent
        availableLines: itip.get_lines()
    }
}

