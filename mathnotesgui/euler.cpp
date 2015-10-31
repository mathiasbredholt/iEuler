#include "euler.h"

#define EULER_PORT 41000
#define GUI_PORT 42000

Euler::Euler(QObject *parent) : QObject(parent)
{
//     Start iEuler
    proc = new QProcess(this);
    proc->start("python3 start.py");
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));

    // Init socket
    socket = new QUdpSocket(this);
    socket->bind(QHostAddress::LocalHost, GUI_PORT);

    connect(socket, SIGNAL(readyRead()), this, SLOT(readPendingDatagrams()));
}

void Euler::restartCore()
{
    terminate();
    proc = new QProcess(this);
    proc->start("python3 start.py");
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));
}

void Euler::terminate()
{
    proc->terminate();
}

void Euler::processDatagram(QByteArray datagram)
{
    char cmd = datagram.at(0);

    if (cmd == Euler::RENDER) {
        int tabIndex;
        int index;
        QString latexString;

        tabIndex = (int) datagram.at(1);

        index = (int) datagram.at(2) << 8;
        index += (int) datagram.at(3) & 0xFF;

        latexString = QString::fromUtf8(datagram.remove(0, 4));

        emit receivedLatexString(tabIndex, index, latexString);
    } else if (cmd == Euler::MATH_STR) {
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

    char cmd = Euler::PREVIEW;
    if (evaluate) cmd = Euler::EVALUATE;

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
    datagram.append(Euler::OPEN);
    datagram.append(path.toUtf8());
    writeDatagram(datagram);
}

void Euler::sendSaveFileRequest(QString path)
{
    QByteArray datagram;
    datagram.append(Euler::SAVE);
    datagram.append(path.toUtf8());
    writeDatagram(datagram);
}

void Euler::sendExportRequest(QString path)
{
    QByteArray datagram;
    datagram.append(Euler::EXPORT);
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

void Euler::readStandardOutput()
{

}

void Euler::readStandardError()
{
    QString err = proc->readAllStandardError();
    qDebug() << "python error: \n" << err;
    QMessageBox msgBox;
    msgBox.setText("The iEuler core has crashed.");
    msgBox.setInformativeText("Restart?");
    msgBox.setStandardButtons(QMessageBox::Ignore | QMessageBox::Reset);
    msgBox.setDefaultButton(QMessageBox::Reset);
    if (err.contains("TypeError")) {
        int ret = msgBox.exec();
        if (ret == QMessageBox::Reset) restartCore();
    }
}
