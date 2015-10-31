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
        1: Evaluate
        2: Open file
        3: Save file
        4: Render
        5: Load math string
    */

    char cmd = datagram.at(0);

    if (cmd == 4) {
        int index;
        QString latexString;

        index = (int) datagram.at(1) << 8;
        index += (int) datagram.at(2) & 0xFF;

        latexString = QString::fromUtf8(datagram.remove(0, 3));

        emit receivedLatexString(index, latexString);
    } else if (cmd == 5) {
        int index;
        QString mathString;

        index = (int) datagram.at(1) << 8;
        index += (int) datagram.at(2) & 0xFF;

        mathString = QString::fromUtf8(datagram.remove(0, 3));

        emit receivedMathString(index, mathString);
    }

}

void Euler::sendMathString(int index, QString mathString, bool evaluate)
{
    QByteArray datagram;

    char cmd = 0;
    if (evaluate) cmd = 1;

    // Control command
    datagram.append(cmd);

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
