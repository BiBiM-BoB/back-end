import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { Tool } from '../models/schemas/tool';

@Injectable()
export class ToolService {
    constructor(
        @InjectRepository(Tool)
        private toolRepository: Repository<Tool>,
      ) {}
    
      async findAll(): Promise<Tool[]> {
        return await this.toolRepository.find();
      }
}