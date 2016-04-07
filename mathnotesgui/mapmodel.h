#ifndef MAPMODEL_H
#define MAPMODEL_H

#include <QAbstractTableModel>
#include <QMap>
#include <QDebug>

class MapModel : public QAbstractTableModel
{
    Q_OBJECT
public:

    enum MapRoles {
        KeyRole = Qt::UserRole + 1,
        ValueRole
    };

    explicit MapModel(QObject *parent = 0);
    int rowCount(const QModelIndex& parent = QModelIndex()) const;
    int columnCount(const QModelIndex& parent = QModelIndex()) const;
    QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const;
    void setMap(QMap<QString, QVariant>* map);

private:
    QMap<QString, QVariant>* _map;
};

#endif // MAPMODEL_H
