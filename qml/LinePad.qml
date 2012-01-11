
import QtQuick 1.0
import QtMobility.feedback 1.1

Rectangle {
    id: linePad
    property alias currentLine: inputLine.text

    /* List of available lines - will be filled w/ real data by LineSheet */
    property variant availableLines: ['59A', '63A', '58']

    property variant matches: availableLines

    onMatchesChanged: {
        if (matches !== undefined) {
            if (matches.length == 1) {
                inputLine.text = matches[0];
            }
        }
    }

    function getMatches(prefix) {
        var result = [];

        for (var i in availableLines) {
            var line = availableLines[i];
            if (line.indexOf(prefix) == 0) {
                result.push(line);
            }
        }

        return result;
    }

    height: 800
    width: 480

     HapticsEffect {
         id: buttonFeedback

         /**
          * Ideally we would use ThemeEffect here,
          * but on Harmattan it has no effect (sic)
          **/

         attackIntensity: 0.5
         attackTime: 100
         intensity: 1.0
         duration: 50
         fadeTime: 0
         fadeIntensity: 0.0
     }

    Text {
        id: inputLine
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        height: 100
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }

        font {
            pixelSize: height * .9
            bold: true
        }

        text: ''
        onTextChanged: {
            if (text != '') {
                linePad.matches = linePad.getMatches(text);
            } else {
                linePad.matches = linePad.availableLines;
            }
        }

        Image {
            source: 'image://theme/icon-m-toolbar-backspace'
            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                margins: 20
            }

            MouseArea {
                anchors {
                    fill: parent
                    margins: -(inputLine.height - height)/2
                }
                onClicked: {
                    buttonFeedback.start()
                    inputLine.text = ''
                }
            }
        }
    }

    Item {
        id: inputState
        property bool isMetro: inputLine.text[0] == 'U'
    }

    Repeater {
        model: [1,2,3, 4,5,6, 7,8,9, 'A',0,'B', 'D','U','VRT', 'O','N','WLB']

        Rectangle {
            id: inputElement
            property variant ch: modelData
            property bool isCandidate

            isCandidate: {
                for (var i in linePad.matches) {
                    if (ch == matches[i][inputLine.text.length]) {
                        return true;
                    } else if ((ch == 'VRT' || ch == 'WLB') && inputLine.text == '') {
                        return true;
                    }
                }

                return false;
            }

            opacity: isCandidate?1:.15
            Behavior on opacity { PropertyAnimation { } }

            color: {
                if (inputState.isMetro) {
                    switch (ch) {
                        case 1: return '#E20A16';
                        case 2: return '#764785';
                        case 3: return '#F76013';
                        case 4: return '#008131';
                        case 6: return '#88471F';
                    }
                }
                return (index%2?'#ddd':'#eee');
            }
            width: parent.width/3
            height: (parent.height-inputLine.height)/6
            x: width*(index%3)
            y: inputLine.height + height*parseInt(index/3)

            Text {
                anchors.centerIn: parent
                text: modelData
                font {
                    pixelSize: parent.height * .5
                    bold: true
                }
                color: {
                    if (inputState.isMetro) {
                        return 'white';
                    } else if (inputElement.isCandidate) {
                        return 'black';
                    }

                    return '#ddd';
                }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    buttonFeedback.start()
                    inputLine.text += modelData
                }
            }
        }
    }
}

