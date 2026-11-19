# Order API fixture
Framework-neutral Node application handler. request.session is trusted server session context. request.body is untrusted client input. rows are records in the server repository. Response status must remain 401 for no session, 404 for absent/foreign record, 200 for own record. No server is needed for tests; run node --test. Change only handler and its tests.
