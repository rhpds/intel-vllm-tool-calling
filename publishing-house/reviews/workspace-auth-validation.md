# Publishing House authoring credential correction

The inherited authoring bootstrap now uses verified system trust or an approved enterprise CA bundle via `PH_CA_BUNDLE`. Credential-bearing redirects and HTTP/TLS failures stop setup. Complete auth JSON is atomically installed in a private `0700` directory with `0600` file permissions; existing permissions are repaired and no key values or prefixes are logged. Configure author Git identity separately.

The regression suite executes the actual devfile's embedded bootstrap with synthetic credentials and mocked transport. It checks TLS trust settings, HTTP/TLS failures, rejected redirects, enterprise CA selection, a permissive umask, atomic/private storage, existing permission repair, incomplete-response preservation and non-disclosing error handling. GitHub `workspace-auth` CI runs these tests; it is not full learner E2E or model acceptance.

No real PH credential issuance, credential copying or learner permission grant is performed by these tests. The lab's functional validation and PH review gates remain separate. PH owns generated AgnosticV and catalog publication. The PH template owner should review the same inherited defects in the source scaffold. No PH approval or stage transition is asserted.
