#-------------------------------------------------
#
# Project created by QtCreator 2015-09-23T13:11:33
#
#-------------------------------------------------

QT       += core gui
QT       += network
QT       += webchannel
QT       += webenginewidgets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = mathnotesgui
TEMPLATE = app


SOURCES += \
    main.cpp \
    mainwindow.cpp \
    cmdpanel.cpp \
    plotview3d.cpp \
    euler.cpp \
    renderer.cpp \
    mathwidget.cpp \
    paragraph.cpp \
    mathedit.cpp \
    cmdpanelitem.cpp \
    util.cpp

HEADERS  += \
    mainwindow.h \
    cmdpanel.h \
    plotview3d.h \
    euler.h \
    renderer.h \
    mathwidget.h \
    paragraph.h \
    mathedit.h \
    cmdpanelitem.h \
    util.h

FORMS    += \
    mainwindow.ui

RESOURCES += \
    katex.qrc

DISTFILES +=
