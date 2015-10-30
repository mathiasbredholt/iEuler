#ifndef EULER_H
#define EULER_H

#include <QObject>
#include <QProcess>
#include <QUdpSocket>

class Euler : public QObject
{
    Q_OBJECT
public:
    explicit Euler(QObject *parent = 0);
    void sendMathString(int index, QString mathString, bool evaluate);

signals:
    void receivedLatexString(int index, QString latexString);

public slots:

private:
    QProcess *proc;
    QUdpSocket *socket;

    void processDatagram(QByteArray datagram);

private slots:
    void readPendingDatagrams();
    void writeDatagram(QByteArray datagram);
};

#endif // EULER_H
