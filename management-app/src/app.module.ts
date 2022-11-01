import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { MongooseModule } from '@nestjs/mongoose';
import { SecurityResult, SecurityResultSchema } from './models/schemas/security_result.schema'
import { SecurityResultController } from './controllers/security_result/security_result.controller';
import { SecurityResultService } from './services/security_result.service';
import { ToolModule } from './modules/tool.module';
import { Tool } from './models/schemas/tool';
import { ToolService } from './services/tool.service';

@Module({
  imports: [
    MongooseModule.forRoot("mongodb://localhost:27017"),
    TypeOrmModule.forRoot({
      type: 'mysql',
      host: 'localhost',
      port: 3306,
      username: 'bibimbob',
      password: '1q2w3e4r!',
      database: 'devsecopsdb',
      entities: [Tool], // Tool 제거
      synchronize: false,
    }),
    ToolModule,
    MongooseModule.forFeature([{name: SecurityResult.name, schema: SecurityResultSchema}]),
  ],
  controllers: [AppController, SecurityResultController],
  providers: [AppService, SecurityResultService, ToolService], // ToolService 제거
})
export class AppModule {}