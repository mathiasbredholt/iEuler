#include "euler.h"

#define EULER_PORT 41000
#define GUI_PORT 42000

Euler::Euler(QObject *parent) : QObject(parent)
{
//     Start iEuler
    proc = new QProcess(this);
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));
    proc->start("python3 -u start.py");

    // Init socket
    socket = new QUdpSocket(this);
    socket->bind(QHostAddress::LocalHost, GUI_PORT);

    connect(socket, SIGNAL(readyRead()), this, SLOT(readPendingDatagrams()));
}

void Euler::restartCore()
{
    terminate();
    proc = new QProcess(this);
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));
    proc->start("python3 -u start.py");
    hasCrashed = false;
}

void Euler::terminate()
{
    proc->kill();
}

void Euler::processDatagram(QByteArray datagram)
{
    if (datagram.size() > 0) {
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
        } else if (cmd == Euler::PLOT) {
            int tabIndex;
            int index;
            QString path;

            tabIndex = (int) datagram.at(1);

            index = (int) datagram.at(2) << 8;
            index += (int) datagram.at(3) & 0xFF;

            path = QString::fromUtf8(datagram.remove(0, 4));

            emit receivedPlot(tabIndex, index, path);
        } else if (cmd == Euler::WORKSP) {
            int tabIndex;
            int index;
            QJsonObject workspace;

            tabIndex = (int) datagram.at(1);

            index = (int) datagram.at(2) << 8;
            index += (int) datagram.at(3) & 0xFF;

            workspace = QJsonDocument::fromJson(datagram.remove(0, 4)).object();
            emit receivedWorkspace(tabIndex, index, workspace.toVariantMap());
        }
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
    while (proc->canReadLine()) {
        QString msg = QString::fromLocal8Bit(proc->readLine());

//        qDebug() << "iEuler: " + msg;
        emit receivedMsg(msg);
    }
}

void Euler::readStandardError()
{
    // Print error message
    qDebug() << "python error:";
    QString error = proc->readAllStandardError();
    QStringList errorList = error.split("\n");
    for (int i = 0; i < errorList.size(); ++i)
        qDebug() << errorList.at(i);

    emit receivedError(error);

    if (!hasCrashed) {
        hasCrashed = true;
        QMessageBox msgBox;
        msgBox.setText("The iEuler core has crashed.");
        msgBox.setInformativeText("Restart?");
        msgBox.setStandardButtons(QMessageBox::Ignore | QMessageBox::Reset);
        msgBox.setDefaultButton(QMessageBox::Reset);

        int ret = msgBox.exec();
        if (ret == QMessageBox::Reset) restartCore();
    }

}
