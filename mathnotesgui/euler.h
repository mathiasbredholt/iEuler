#ifndef EULER_H
#define EULER_H

#include <QObject>
#include <QProcess>
#include <QUdpSocket>
#include <QMessageBox>

class Euler : public QObject
{
    Q_OBJECT
public:
    explicit Euler(QObject *parent = 0);
    void restartCore();
    void terminate();
    void sendMathString(int tabIndex, int index, QString mathString, bool evaluate);
    void sendOpenFileRequest(QString path);
    void sendSaveFileRequest(QString path);
    void sendExportRequest(QString path);

signals:
    void receivedLatexString(int tabIndex, int index, QString latexString);
    void receivedMathString(int tabIndex, int index, QString mathString);

public slots:

private:
    QProcess *proc;
    QUdpSocket *socket;

    void processDatagram(QByteArray datagram);

private slots:
    void readPendingDatagrams();
    void writeDatagram(QByteArray datagram);
    void readStandardOutput();
    void readStandardError();
};

#endif // EULER_H
