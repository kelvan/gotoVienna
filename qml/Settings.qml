import QtQuick 1.1
import com.nokia.meego 1.0
import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: settingsTools

    ToolBarLayout {
        id: settingsTools
        x: 0
        y: 0
        ToolIcon { iconId: "toolbar-back"; onClicked: { menu.close(); pageStack.pop(null,false); } }
    }

    Flickable {
        id: settingsContent
        anchors.fill: parent
        anchors.margins: UIConstants.DEFAULT_MARGIN

        //contentHeight: content_column.height + 2 * UIConstants.DEFAULT_MARGIN
        flickableDirection: Flickable.VerticalFlick

        Component.onCompleted: {
            var updateAvailable = config.checkStationsUpdate();
            if (updateAvailable) {
                btnUpdate.color = "green"
            }
        }

        Column {
            id: content_column
            spacing: UIConstants.DEFAULT_MARGIN
            width: parent.width

            Text {
                text: qsTr("Settings")
                font.pixelSize: UIConstants.FONT_XLARGE
                color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                anchors.left: parent.left
            }

            SettingsHeader {
                text: 'Location'
            }

            Row {
                anchors.left: parent.left
                anchors.right: parent.right
                Text {
                    text: "Enable GPS"
                    anchors.left: parent.left
                    font.pixelSize: UIConstants.FONT_LARGE
                    color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                    anchors.verticalCenter: parent.verticalCenter
                }
                Switch {
                    id: gpsEnable
                    anchors.right: parent.right
                    checked: config.getGpsEnabled()

                    onCheckedChanged: {
                        var gps = config.setGpsEnabled(checked);
                        if (gps !== '') {
                            // Unable to set config
                            console.log(gps);
                            checked=!checked;
                        } else {
                            positionSource.active = checked;
                        }
                        if (checked) {
                            positionSource.start();
                        } else {
                            positionSource.stop();
                        }
                    }
                }
            }

            InfoDialog {
                id:updateDialog
            }

            SettingsHeader {
                text: 'Station List'
            }

            Button {
                id: btnUpdate
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Update stations"
                width: parent.width * .7

                Component.onCompleted: {
                    if (config.checkStationsUpdate()) {
                        btnUpdate.color = "green"
                    }
                }

                onClicked: {
                    var updateAvailable = config.checkStationsUpdate();
                    if (updateAvailable) {
                        var updated = config.updateStations();
                        if (updated !== '') {
                            updateDialog.text = "Stations updated\nPlease restart app"
                            txtLastUpdate.text = updated
                        } else {
                            updateDialog.text = "[UpdateError]:\nTry again later or send me an email:\n<gotovienna@logic.at>"
                        }
                    } else {
                        updateDialog.text = "No updates available";
                    }
                    updateDialog.open();
                }
            }

            InfoDialog {
                id:clearDialog
            }

            SettingsHeader {
                text: 'Cache'
            }

            Button {
                id: btnClearCache
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Clear"
                width: parent.width * .7

                Component.onCompleted: {
                    if (config.checkClearedCache()) {
                        btnClearCache.color = "green"
                    }
                }

                onClicked: {
                    var cleared = config.clearCache();
                    if (cleared) {
                        clearDialog.text = "Cache cleared"
                    } else {
                        updateDialog.text = "[ClearError]:\nTry again later or send me an email:\n<gotovienna@logic.at>"
                    }
                    clearDialog.open();
                }
            }

            Row {
                anchors.left: parent.left
                anchors.right: parent.right
                Text {
                    anchors.left: parent.left
                    text: "Last updated:"
                    font.pixelSize: UIConstants.FONT_LSMALL
                    color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    id: txtLastUpdate
                    anchors.right: parent.right
                    text: config.getLastUpdate()
                    font.pixelSize: UIConstants.FONT_LSMALL
                    color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }
    }
}
