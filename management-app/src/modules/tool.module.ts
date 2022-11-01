import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { Tool } from 'src/models/schemas/tool';
import { ToolService } from 'src/services/tool.service';

@Module({
  imports: [TypeOrmModule.forFeature([Tool])],
  exports: [ToolService, TypeOrmModule],
  controllers: [],
  providers: [ToolService]
})
export class ToolModule {}