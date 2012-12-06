import QtQuick 1.1
import com.nokia.meego 1.0
import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: settingsTools

    ToolBarLayout {
        id: settingsTools
        ToolIcon { iconId: "toolbar-back"; onClicked: { pageStack.pop(null,false); } }
    }


    InfoDialog {
        id:infoDialog
    }

    Flickable {
        id: settingsContent
        anchors.fill: parent
        anchors.margins: UIConstants.DEFAULT_MARGIN

        //contentHeight: content_column.height + 2 * UIConstants.DEFAULT_MARGIN
        flickableDirection: Flickable.VerticalFlick

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
                Column {
                    id: textColumn
                    Text {
                        text: "Enable GPS"
                        font.pixelSize: UIConstants.FONT_LARGE
                        color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                    }
                }
                Column {
                    width: parent.width - textColumn.width
                    Switch {
                        anchors.right: parent.right
                        id: gpsEnable
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
//                     if (config.checkStationsUpdate()) {
//                         btnUpdate.text = "Update stations (new)"
//                     }
                }

                onClicked: {
                    var updateAvailable = config.checkStationsUpdate();
                    if (updateAvailable) {
                        var updated = config.updateStations();
                        if (updated !== '') {
                            infoDialog.text = "Stations updated\nPlease restart app"
                            txtLastUpdate.text = updated
                        } else {
                            infoDialog.text = "[UpdateError]:\nTry again later or send me an email:\n<gotovienna@logic.at>"
                        }
                    } else {
                        infoDialog.text = "No updates available";
                    }
                    infoDialog.open();
                }
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
//                     if (config.checkClearedCache()) {
//                         btnClearCache.color = "green"
//                     }
                }

                onClicked: {
                    var cleared = config.clearCache();
                    if (cleared) {
                        infoDialog.text = "Cache cleared"
                    } else {
                        infoDialog.text = "[ClearError]:\nTry again later or send me an email:\n<gotovienna@logic.at>"
                    }
                    infoDialog.open();
                }
            }

            Row {
                anchors.left: parent.left
                anchors.right: parent.right
                Text {
                    text: "Last updated: "
                    font.pixelSize: UIConstants.FONT_LSMALL
                    color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    id: txtLastUpdate
                    text: config.getLastUpdate()
                    font.pixelSize: UIConstants.FONT_LSMALL
                    color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }
    }
}
