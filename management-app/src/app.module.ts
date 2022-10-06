import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MongooseModule } from '@nestjs/mongoose';
import { SecurityResult, SecurityResultSchema } from './models/schemas/security_result.schema'
import { SecurityResultController } from './controllers/security_result/security_result.controller';
import { SecurityResultService } from './services/security_result.service';

@Module({
  imports: [
    MongooseModule.forRoot("mongodb://localhost:27017"),
    MongooseModule.forFeature([{name: SecurityResult.name, schema: SecurityResultSchema}]),
  ],
  controllers: [AppController, SecurityResultController],
  providers: [AppService, SecurityResultService],
})
export class AppModule {}