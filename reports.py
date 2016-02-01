import HTML

def writeParamsToHTML(objectId, scopeIds, listOfParameters, tableId):
  global f
  tArgs= []
  for i in listOfParameters :
    paramValue = AdminConfig.showAttribute(objectId,i)
    tArgs.append(paramValue)
  tArgs.append(scopeIds)
  tableId.rows.append(tArgs)
    
    
def writeQueuesByScope(scopeIds, qParams, tableId):
  global f
  for s in scopeIds :
    try :
      queues = AdminTask.listWMQQueues(s).splitlines()
      scope = s.split('|')[0].split('(')[1]
      for q in queues :
        tArgs = []
        for p in qParams :
          paramValue = AdminConfig.showAttribute(q,p)
          tArgs.append(paramValue)
        tArgs.append(scope)
        tableId.rows.append(tArgs)
    except :
      print sys.exc_info()
  

HTMLFILE = 'WASreport.html'
f = open(HTMLFILE, 'w')
            
queueT = HTML.Table(header_row=['Name', 'JNDI name', 'MQ Queue manager', 'MQ Queue name', 'Scope'])
queueParams = ["name", "jndiName", "baseQueueManagerName", "baseQueueName"]

cell = AdminConfig.getid('/Cell:/').splitlines()
nodes = AdminConfig.getid('/Node:/').splitlines()
servers = AdminConfig.getid('/Server:/').splitlines()

'''writeQueuesByScope(cell, queueParams, queueT)
writeQueuesByScope(nodes, queueParams, queueT)'''
writeQueuesByScope(servers, queueParams, queueT)


htmlcode = str(queueT)
f.write(htmlcode)
f.write('<p>')


dbT = HTML.Table(header_row=['Name', 'JNDI name', 'Provider', 'JAAS Alias', 'Scope'])
dbParams = ['name', 'jndiName', 'provider', 'authDataAlias']

'''
datasourcesId = AdminConfig.list('DataSource').splitlines()
for i in datasourcesId :
    dsScope = i.split('(')[1].split('|')[0]
    writeParamsToHTML(i, dsScope, dbParams, dbT)
'''
f.close()