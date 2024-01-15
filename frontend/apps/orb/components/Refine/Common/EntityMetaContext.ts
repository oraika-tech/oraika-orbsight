import { createContext } from 'react';
import { EntityOptions } from './CommonModels';

export const EntityMetaContext = createContext<EntityOptions>({ fields: [] });
