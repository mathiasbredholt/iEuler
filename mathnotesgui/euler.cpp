#include "euler.h"

#define EULER_PORT 41000
#define GUI_PORT 42000

Euler::Euler(QObject *parent) : QObject(parent)
{
    // Start iEuler
//    proc = new QProcess(this);
//    proc->start("python3 start.py -gui");

    // Init socket
    socket = new QUdpSocket(this);
    socket->bind(QHostAddress::LocalHost, GUI_PORT);

    connect(socket, SIGNAL(readyRead()), this, SLOT(readPendingDatagrams()));
}

void Euler::processDatagram(QByteArray datagram)
{
    /*
        Command reference
        0: Preview
            0   cmd
            1   tab index
            2   index MSB
            3   index LSB
            [4] math string
        1: Evaluate
            0   cmd
            1   tab index
            2   index MSB
            3   index LSB
            [4] math string
        2: Open file
            0   cmd
            [1] path
        3: Save file
            0   cmd
            [1] path
        4: Render
            0   cmd
            1   tab index
            2   index MSB
            3   index LSB
            [4] latex string
        5: Load math string
            0   cmd
            1   tabIndex
            2   index MSB
            3   index LSB
            [4] math string
    */

    char cmd = datagram.at(0);

    if (cmd == 4) {
        int tabIndex;
        int index;
        QString latexString;

        tabIndex = (int) datagram.at(1);

        index = (int) datagram.at(2) << 8;
        index += (int) datagram.at(3) & 0xFF;

        latexString = QString::fromUtf8(datagram.remove(0, 4));

        emit receivedLatexString(tabIndex, index, latexString);
    } else if (cmd == 5) {
        int tabIndex;
        int index;
        QString mathString;

        tabIndex = (int) datagram.at(1);

        index = (int) datagram.at(2) << 8;
        index += (int) datagram.at(3) & 0xFF;

        mathString = QString::fromUtf8(datagram.remove(0, 4));

        emit receivedMathString(tabIndex, index, mathString);
    }

}

void Euler::sendMathString(int tabIndex, int index, QString mathString, bool evaluate)
{
    QByteArray datagram;

    char cmd = 0;
    if (evaluate) cmd = 1;

    // Control command
    datagram.append(cmd);

    datagram.append((char) tabIndex);

    // Encode line index to datagram
    datagram.append((char) index >> 8);
    datagram.append((char) index & 0xFF);

    // Append command
    datagram.append(mathString.toUtf8());

    writeDatagram(datagram);
}

void Euler::sendOpenFileRequest(QString path)
{
    QByteArray datagram;
    char cmd = 2;

    datagram.append(cmd);
    datagram.append(path.toUtf8());

    writeDatagram(datagram);
}

void Euler::sendSaveFileRequest(QString path)
{
    QByteArray datagram;
    char cmd = 3;

    datagram.append(cmd);
    datagram.append(path.toUtf8());

    writeDatagram(datagram);
}

void Euler::readPendingDatagrams()
{
    while (socket->hasPendingDatagrams()) {
        QByteArray datagram;
        datagram.resize(socket->pendingDatagramSize());
        QHostAddress addr;
        quint16 port;

        socket->readDatagram(datagram.data(), datagram.size(), &addr, &port);
        processDatagram(datagram);
    }
}

void Euler::writeDatagram(QByteArray datagram)
{
    quint16 port = EULER_PORT;
    socket->flush();
    socket->writeDatagram(datagram, QHostAddress::LocalHost, port);
}
