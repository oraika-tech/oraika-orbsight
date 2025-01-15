cube(`ProcessedDataViewV1`, {
    sql: `SELECT * FROM data_view.processed_data_view_v1`,

    preAggregations: {
        // Pre-Aggregations definitions go here
        // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
    },

    joins: {

        Categories: {
            sql: `${CUBE.processedDataId} = ${Categories.id}`,
            relationship: `hasMany`
        },

        TaxonomyTerms: {
            sql: `${CUBE.processedDataId} = ${TaxonomyTerms.id}`,
            relationship: `hasMany`
        },

        TaxonomyTags: {
            sql: `${CUBE.processedDataId} = ${TaxonomyTags.id}`,
            relationship: `hasMany`
        },

        People: {
            sql: `${CUBE.processedDataId} = ${People.id}`,
            relationship: `hasMany`
        }

    },

    measures: {

        count: {
            type: `count`,
            drillMembers: [observerName, entityName, authorName, referenceId, conversationId]
        },

        avgRating: {
            sql: `ROUND(AVG(rating::INTEGER), 1)`,
            type: `number`,
        },

        uniqueConversationCount: {
            sql: `conversation_id`,
            type: `countDistinct`,
        },

        uniqueAuthorCount: {
            sql: `author_name`,
            type: `countDistinct`,
        }

    },

    dimensions: {

        rawDataId: {
            sql: `raw_data_id`,
            type: `number`,
            primaryKey: true,
            shown: true
        },

        processedDataId: {
            sql: `processed_data_id`,
            type: `number`,
            primaryKey: true,
            shown: true
        },

        observerType: {
            sql: `observer_type`,
            type: `string`
        },

        observerName: {
            sql: `observer_name`,
            type: `string`
        },

        entityName: {
            sql: `entity_name`,
            type: `string`
        },

        rating: {
            sql: `rating`,
            type: `string`
        },

        textLang: {
            sql: `text_lang`,
            type: `string`
        },

        authorName: {
            sql: `author_name`,
            type: `string`
        },

        referenceId: {
            sql: `reference_id`,
            type: `string`
        },

        url: {
            sql: `url`,
            type: `string`
        },

        conversationId: {
            sql: `conversation_id`,
            type: `string`
        },

        textHash: {
            sql: `text_hash`,
            type: `string`
        },

        emotion: {
            sql: `emotion`,
            type: `string`
        },

        rawText: {
            sql: `raw_text`,
            type: `string`
        },

        taxonomyTags: {
            sql: `array_to_string(taxonomy_tags, ', ')`,
            type: `string`
        },

        people: {
            sql: `array_to_string(people, ', ')`,
            type: `string`
        },

        eventTime: {
            sql: `event_time`,
            type: `time`
        }
    },

    dataSource: `default`
});


cube(`Categories`, {
    sql: `SELECT processed_data_id, UNNEST(categories) as category FROM data_view.processed_data_view_v1`,

    dimensions: {

        id: {
            sql: `processed_data_id`,
            type: `string`,
            primaryKey: true
        },

        category: {
            sql: `category`,
            type: `string`
        }

    },

    dataSource: `default`
});

cube(`TaxonomyTerms`, {
    sql: `SELECT processed_data_id, UNNEST(taxonomy_terms) as taxonomy_term FROM data_view.processed_data_view_v1`,

    dimensions: {

        id: {
            sql: `processed_data_id`,
            type: `string`,
            primaryKey: true
        },

        taxonomyTerm: {
            sql: `taxonomy_term`,
            type: `string`
        }

    },

    dataSource: `default`
});

cube(`TaxonomyTags`, {
    sql: `SELECT processed_data_id, UNNEST(taxonomy_tags) as taxonomy_tag FROM data_view.processed_data_view_v1`,

    dimensions: {

        id: {
            sql: `processed_data_id`,
            type: `string`,
            primaryKey: true
        },

        taxonomyTag: {
            sql: `taxonomy_tag`,
            type: `string`
        }

    },

    dataSource: `default`
});


cube(`People`, {
    sql: `SELECT processed_data_id, UNNEST(people) as people_name FROM data_view.processed_data_view_v1`,

    dimensions: {

        id: {
            sql: `processed_data_id`,
            type: `string`,
            primaryKey: true
        },

        name: {
            sql: `people_name`,
            type: `string`
        }

    },

    dataSource: `default`
});
