module.exports = {
  allowUngroupedWithoutPrimaryKey: true,
  contextToAppId: ({ securityContext }) =>
    `CUBEJS_APP_$${securityContext ? securityContext.tenantCode : 'oraika'}`,
  contextToOrchestratorId: ({ securityContext }) =>
    `CUBEJS_APP_$${securityContext ? securityContext.tenantCode : 'oraika'}`,
  driverFactory: ({ securityContext }) => ({
    type: 'postgres',
    database: `orb_tenant_$${securityContext ? securityContext.tenantCode : 'oraika'}`,
    host: '${db_host}',
    user: '${db_user}',
    password: '${db_pass}',
    port: '5432',
  }),
  // scheduledRefreshContexts should return an array of `securityContext`
  scheduledRefreshContexts: () => [
    { securityContext: { tenantCode: 'oraika' } },
  ]
};